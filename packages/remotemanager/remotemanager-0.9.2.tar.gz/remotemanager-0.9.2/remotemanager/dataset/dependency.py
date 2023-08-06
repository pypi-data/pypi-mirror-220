import os
import warnings

from remotemanager.storage.remotefunction import cached_functions
from remotemanager.logging import LoggingMixin
from remotemanager.storage.sendablemixin import SendableMixin


class Dependency(SendableMixin, LoggingMixin):

    _do_not_package = ["_network"]

    def __init__(self):
        self._logger.info("new Dependency created")

        self._network = []
        self._parents = []
        self._children = []

    def add_edge(self, primary, secondary):
        pair = (primary, secondary)
        if pair not in self._network:
            self._logger.info(f"adding new edge {pair}")

            self._parents.append(primary.short_uuid)
            self._children.append(secondary.short_uuid)

            self._network.append(pair)

    @property
    def network(self):
        return self._network

    def get_children(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._parents)):
            if self._parents[i] == uuid:
                tmp.append(self.network[i][1])

        return tmp

    def get_parents(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._children)):
            if self._children[i] == uuid:
                tmp.append(self.network[i][0])

        return tmp

    @property
    def ds_list(self):

        datasets = []
        for pair in self.network:
            for ds in pair:
                if ds not in datasets:
                    datasets.append(ds)

        return datasets

    def remove_run(self, id: bool = False) -> bool:
        out = []
        for ds in self.ds_list:
            out.append(ds.remove_run(id=id, dependency_call=True))

        return all(out)

    def clear_runs(self) -> None:
        for ds in self.ds_list:
            ds.clear_runs(dependency_call=True)

    def clear_results(self, wipe) -> None:
        for ds in self.ds_list:
            ds.clear_results(wipe, dependency_call=True)

    def wipe_local(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.wipe_local(files_only=files_only, dependency_call=True)

    def wipe_remote(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.wipe_remote(files_only=files_only, dependency_call=True)

    def hard_reset(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.hard_reset(files_only=files_only, dependency_call=True)

    def append_run(
        self, caller, chain_run_args, run_args, force, lazy, *args, **kwargs
    ):
        """
        Appends runs with the same args to all datasets

        Args:
            caller:
                (Dataset): The dataset which defers to the dependency
            chain_run_args (bool):
                for dependency runs, will not propagate run_args to other datasets in
                the chain if False (defaults True)
            run_args (dict):
                runner arguments
            *args:
                append_run args
            **kwargs:
                append_run keyword args

        Returns:
            None
        """
        self._logger.info(f"appending run from {caller}")

        datasets = self.ds_list
        self._logger.info(f"There are {len(datasets)} datasets in the chain")

        if chain_run_args:
            self._logger.info("chain_args is True, propagating")
            kwargs.update(run_args)

        for ds in datasets:
            if ds == caller:
                caller_args = {k: v for k, v in kwargs.items()}
                caller_args.update(run_args)
                ds.append_run(
                    dependency_call=True, force=force, lazy=lazy, *args, **caller_args
                )
            else:
                ds.append_run(
                    dependency_call=True, force=force, lazy=lazy, *args, **kwargs
                )

        for ds in datasets:
            parents = self.get_parents(ds)
            if len(parents) > 1:
                warnings.warn(
                    "Multiple parents detected. "
                    "Variable passing in this instance is unstable!"
                )
            for parent in parents:
                # TODO this is broken with multiple parents
                lstr = (
                    f"import os.path\n"
                    f'if os.path.getmtime("'
                    f'{parent.runners[-1].runfile.name}") > '
                    f'os.path.getmtime("'
                    f'{parent.runners[-1].resultfile.name}"):\n'
                    f'\traise RuntimeError("outdated '
                    f'result file for parent")\n'
                    f'repo.loaded = repo.load("'
                    f'{parent.runners[-1].resultfile.name}")'
                )
                ds.runners[-1]._dependency_info["parent_import"] = lstr

            tmp = []
            for child in self.get_children(ds):
                runner = child.runners[-1]
                tmp.append(
                    f"{child.url.submitter} {runner.jobscript.name} "
                    f"2>> {runner.errorfile.name}"
                )

            ds.runners[-1]._dependency_info["child_submit"] = tmp

            if not lazy:
                ds.database.update(ds.pack())

    def finish_append(self) -> None:
        for ds in self.ds_list:
            ds.finish_append(dependency_call=True)

    def run(
        self,
        dry_run: bool = False,
        **run_args,
    ):
        self._logger.info("dependency internal run call")

        ds_store = {}
        for ds in self.ds_list:
            ds_store[ds] = len(ds.runners)

        if not len(set(ds_store.values())) == 1:
            msg = f"Datasets do not have matching numbers of runners!: " f"{ds_store}"
            self._logger.critical(msg)
            raise RuntimeError(msg)

        # we need to write a common repo containing all functions
        first = list(ds_store.keys())[0]

        if not os.path.isdir(first.master_script.local_dir):
            os.makedirs(first.master_script.local_dir)

        with open(first.repofile.local, "w+") as o:
            if len(cached_functions) > 0:
                o.write("### cached functions ###\n")

                for fname, f in cached_functions.items():
                    o.write(f.source + "\n")
                o.write("\n")

            o.write("### primary functions ###\n")
            for ds in ds_store:
                o.write(ds.function.source)
                o.write("\n")

            o.write("\n\n### serialiser functions ###")
            o.write(first.serialiser.dumpfunc())
            o.write("\n")
            o.write(first.serialiser.loadfunc())

        first.transport.queue_for_push(first.repofile)

        # and now a master script to kick off the chains
        # we need the export for ALL datasets
        master_content = [f"export {first.main_dir_env}=$PWD\n"]

        for ds in ds_store:
            # reuse the store as a list of runner uuids for runners_to_update
            ds_store[ds] = []
            for runner in ds.runners:
                ready = runner.stage(
                    python=ds.url.python,
                    repo=f"${first.main_dir_env}/{first.repofile.name}",
                    **run_args,
                )
                if not ready:
                    continue

                # we only need the runlines for the first dataset, since the chaining
                # is handled by the jobscripts
                if ds == first:
                    submitter = ds.url.submitter
                    jobscript = runner.jobscript.relative_remote_path(
                        ds.master_script.remote_dir
                    )
                    jobpath, jobfile = os.path.split(jobscript)

                    runline = f"{submitter} {jobfile} " f"2>> {runner.errorfile.name}"

                    if ds.remote_dir != runner.remote_dir:
                        runline = f"cd {jobpath} && " + runline

                    asynchronous = runner.run_args["asynchronous"]
                    if asynchronous and submitter == "bash":
                        ds._logger.debug('appending "&" for async run')
                        runline += f" &"

                    master_content.append(runline)

                first.transport.queue_for_push(runner.jobscript)
                first.transport.queue_for_push(runner.runfile)

                for file in runner.extra_files["send"]:
                    first.transport.queue_for_push(
                        os.path.split(file)[1],
                        os.path.split(file)[0],
                        runner.remote_dir,
                    )

                ds_store[ds].append(runner.uuid)

        # finally write the script
        with open(first.master_script.local, "w+") as o:
            # need to remove any prior errors
            for dataset in ds_store:
                o.write(f"rm -f *{dataset.short_uuid}*error.out\n")
            o.write("\n")

            for line in master_content:
                o.write(line)
                if first.add_newline:
                    o.write("\n")

        first.transport.queue_for_push(first.master_script)

        if not dry_run:
            first.transport.transfer()

            cmd = (
                f"cd {first.remote_dir} && {first.url.shell} {first.master_script.name}"
            )
            first._run_cmd = first.url.cmd(cmd, asynchronous=True)

            for ds in ds_store:
                ds.set_runner_states("submit pending", ds_store[ds])
        else:
            first.transport.wipe_transfers()
            for ds in ds_store:
                ds.set_runner_states("dry run", ds_store[ds])
