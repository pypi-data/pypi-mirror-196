from typing import Dict, List, IO, Tuple

import spyctl.api as api
import spyctl.cli as cli
import spyctl.config.configs as cfg
import spyctl.filter_resource as filt
import spyctl.resources.clusters as spyctl_clusts
import spyctl.resources.fingerprints as spyctl_fprints
import spyctl.resources.machines as spyctl_machines
import spyctl.resources.deployments as spyctl_deployments
import spyctl.resources.namespaces as spyctl_names
import spyctl.resources.pods as spyctl_pods
import spyctl.resources.nodes as spyctl_nodes
import spyctl.resources.flags as spyctl_flags
import spyctl.resources.policies as spyctl_policies
import spyctl.resources.processes as spyctl_procs
import spyctl.resources.connections as spyctl_conns
import spyctl.spyctl_lib as lib

ALL = "all"


def handle_get(
    resource, name_or_id, st, et, file, latest, exact, output, **filters
):
    if name_or_id and not exact:
        name_or_id += "*" if name_or_id[-1] != "*" else name_or_id
        name_or_id = "*" + name_or_id if name_or_id[0] != "*" else name_or_id
    if resource == lib.CLUSTERS_RESOURCE:
        handle_get_clusters(name_or_id, output, **filters)
    elif resource == lib.FINGERPRINTS_RESOURCE:
        handle_get_fingerprints(
            name_or_id, st, et, output, file, latest, **filters
        )
    elif resource == lib.MACHINES_RESOURCE:
        handle_get_machines(name_or_id, output, **filters)
    elif resource == lib.DEPLOYMENTS_RESOURCE:
        handle_get_deployments(name_or_id, st, et, output, **filters)
    elif resource == lib.NAMESPACES_RESOURCE:
        handle_get_namespaces(name_or_id, st, et, output, **filters)
    elif resource == lib.NODES_RESOURCE:
        handle_get_nodes(name_or_id, st, et, output, **filters)
    elif resource == lib.PODS_RESOURCE:
        handle_get_pods(name_or_id, st, et, output, **filters)
    elif resource == lib.REDFLAGS_RESOURCE:
        handle_get_redflags(name_or_id, st, et, output, **filters)
    elif resource == lib.OPSFLAGS_RESOURCE:
        handle_get_opsflags(name_or_id, st, et, output, **filters)
    elif resource == lib.POLICIES_RESOURCE:
        handle_get_policies(name_or_id, output, file, st, et, **filters)
    elif resource == lib.PROCESSES_RESOURCE:
        handle_get_processes(name_or_id, st, et, output, **filters)
    elif resource == lib.CONNECTIONS_RESOURCE:
        handle_get_connections(name_or_id, st, et, output, **filters)
    else:
        cli.err_exit(f"The 'get' command is not supported for {resource}")


def handle_get_clusters(name_or_id, output: str, **filters: Dict):
    ctx = cfg.get_current_context()
    clusters = api.get_clusters(*ctx.get_api_data())
    clusters = filt.filter_clusters(clusters, **filters)
    output_clusters = []
    for cluster in clusters:
        output_clusters.append(
            {
                "name": cluster["name"],
                "uid": cluster["uid"],
                "cluster_details": {
                    "first_seen": cluster["valid_from"],
                    "last_data": cluster["last_data"],
                    "cluster_id": cluster["cluster_details"]["cluster_uid"],
                },
            }
        )
    if name_or_id:
        output_clusters = filt.filter_obj(
            output_clusters, ["name", "uid"], name_or_id
        )
    if output != lib.OUTPUT_DEFAULT:
        output_clusters = spyctl_clusts.clusters_output(output_clusters)
    cli.show(
        output_clusters,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_clusts.clusters_summary_output},
    )


def handle_get_deployments(name_or_id, st, et, output, **filters):
    ctx = cfg.get_current_context()
    clusters = api.get_clusters(*ctx.get_api_data())
    clusters = filt.filter_clusters(clusters, **filters)
    deployments = api.get_deployments(*ctx.get_api_data(), clusters, (st, et))
    deployments = filt.filter_deployments(deployments, **filters)
    if name_or_id:
        deployments = filt.filter_obj(
            deployments, [[lib.METADATA_FIELD, "name"]], name_or_id
        )
    if output != lib.OUTPUT_DEFAULT:
        deployments = spyctl_deployments.deployments_output(deployments)
    cli.show(
        deployments,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_deployments.deployments_summary_output},
    )


def handle_get_namespaces(name, st, et, output, **filters):
    ctx = cfg.get_current_context()
    clusters = api.get_clusters(*ctx.get_api_data())
    clusters = filt.filter_clusters(clusters, **filters)
    namespaces = api.get_namespaces(*ctx.get_api_data(), clusters, (st, et))
    namespaces = filt.filter_namespaces(
        namespaces, clusters_data=clusters, **filters
    )
    if name:
        namespaces = filt.filter_obj(namespaces, ["namespaces"], name)
    if output != lib.OUTPUT_DEFAULT:
        namespaces = spyctl_names.namespaces_output(namespaces)
    cli.show(
        namespaces,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_names.namespace_summary_output},
    )


def handle_get_machines(name_or_id, output: str, **filters: Dict):
    ctx = cfg.get_current_context()
    machines = api.get_machines(*ctx.get_api_data())
    machines = filt.filter_machines(machines, **filters)
    if name_or_id:
        machines = filt.filter_obj(machines, ["name", "uid"], name_or_id)
    if output != lib.OUTPUT_DEFAULT:
        machines = spyctl_machines.machines_output(machines)
    cli.show(
        machines,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_machines.machines_summary_output},
    )


def handle_get_nodes(name_or_id, st, et, output: str, **filters: Dict):
    ctx = cfg.get_current_context()
    clusters = api.get_clusters(*ctx.get_api_data())
    clusters = filt.filter_clusters(clusters, **filters)
    nodes = api.get_nodes(*ctx.get_api_data(), clusters, (st, et))
    nodes = filt.filter_nodes(nodes, **filters)
    if name_or_id:
        nodes = filt.filter_obj(
            nodes,
            [[lib.METADATA_FIELD, lib.METADATA_NAME_FIELD], lib.ID_FIELD],
            name_or_id,
        )
    if output != lib.OUTPUT_DEFAULT:
        nodes = spyctl_nodes.nodes_output(nodes)
    cli.show(
        nodes,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_nodes.nodes_output_summary},
    )


def handle_get_pods(name_or_id, st, et, output, **filters):
    ctx = cfg.get_current_context()
    clusters = api.get_clusters(*ctx.get_api_data())
    clusters = filt.filter_clusters(clusters, **filters)
    pods = api.get_pods(*ctx.get_api_data(), clusters, (st, et))
    pods = filt.filter_pods(pods)
    if name_or_id:
        pods = filt.filter_obj(
            pods,
            [[lib.METADATA_FIELD, lib.METADATA_NAME_FIELD], lib.ID_FIELD],
            name_or_id,
        )
    if output != lib.OUTPUT_DEFAULT:
        pods = spyctl_pods.pods_output(pods)
    cli.show(
        pods,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_pods.pods_output_summary},
    )


def handle_get_redflags(name_or_id, st, et, output, **filters):
    ctx = cfg.get_current_context()
    flags = api.get_redflags(*ctx.get_api_data(), (st, et))
    flags = filt.filter_redflags(flags, **filters)
    if name_or_id:
        flags = filt.filter_obj(flags, ["short_name", "id"], name_or_id)
    if output != lib.OUTPUT_DEFAULT:
        flags = spyctl_flags.flags_output(flags)
    cli.show(
        flags,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_flags.flags_output_summary},
    )


def handle_get_opsflags(name_or_id, st, et, output, **filters):
    ctx = cfg.get_current_context()
    flags = api.get_opsflags(*ctx.get_api_data(), (st, et))
    flags = filt.filter_opsflags(flags, **filters)
    if name_or_id:
        flags = filt.filter_obj(flags, ["short_name", "id"], name_or_id)
    if output != lib.OUTPUT_DEFAULT:
        flags = spyctl_flags.flags_output(flags)
    cli.show(
        flags,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_flags.flags_output_summary},
    )


def handle_get_fingerprints(
    name_or_id, st, et, output, files: List[IO], latest, **filters
):
    ctx = cfg.get_current_context()
    pol_names_or_uids = filters.pop(lib.POLICY_UID_FIELD, None)
    policy_coverage = filters.pop("policy_coverage", False)
    if pol_names_or_uids:
        policies = __get_policies_from_option(pol_names_or_uids)
    else:
        policies = None
    machines = api.get_machines(*ctx.get_api_data())
    clusters = None
    if cfg.CLUSTER_FIELD in filters or cfg.CLUSTER_FIELD in ctx.get_filters():
        clusters = api.get_clusters(*ctx.get_api_data())
    machines = filt.filter_machines(machines, clusters, **filters)
    muids = [m["uid"] for m in machines]
    if files and len(files) > 1:
        if latest:
            cli.try_log(
                "Unable to use --latest option for multiple input files",
                is_warning=True,
            )
        orig_fprints = api.get_fingerprints(
            *ctx.get_api_data(), muids, (st, et)
        )
        orig_fprints = get_fingerprints_matching_files(orig_fprints, files)
    elif policies and len(policies) > 1:
        if latest:
            cli.try_log(
                "Unable to use --latest option for multiple policies",
                is_warning=True,
            )
        orig_fprints = api.get_fingerprints(
            *ctx.get_api_data(), muids, (st, et)
        )
        orig_fprints = get_fingerprints_matching_policies(
            orig_fprints, policies
        )
    else:
        if files:
            resource_data = lib.load_resource_file(files[0])
            if latest:
                st = __get_latest_timestamp(resource_data)
            filters = lib.selectors_to_filters(resource_data)
            if len(filters) == 0:
                cli.err_exit(
                    f"Unable generate filters from {files[0].name}. Does it"
                    " have a spec field with selectors?"
                )
        elif policies:
            if latest:
                st = __get_latest_timestamp(policies[0])
            filters = lib.selectors_to_filters(policies[0])
        orig_fprints = api.get_fingerprints(
            *ctx.get_api_data(), muids, (st, et)
        )
        orig_fprints = filt.filter_fingerprints(orig_fprints, **filters)
    if policy_coverage:
        fprint_groups, coverage_percentage = calc_policy_coverage(orig_fprints)
    else:
        fingerprints = orig_fprints
        fprint_groups = spyctl_fprints.make_fingerprint_groups(fingerprints)
    if name_or_id:
        cont_fprint_grps, svc_fprint_grps = fprint_groups
        cont_fprint_grps = filt.filter_obj(
            cont_fprint_grps,
            [
                [lib.METADATA_FIELD, lib.IMAGE_FIELD],
                [lib.METADATA_FIELD, lib.IMAGEID_FIELD],
            ],
            name_or_id,
        )
        svc_fprint_grps = filt.filter_obj(
            svc_fprint_grps,
            [
                [lib.METADATA_FIELD, lib.CGROUP_FIELD],
            ],
            name_or_id,
        )
        fprint_groups = (cont_fprint_grps, svc_fprint_grps)
    fprint_groups = filt.filter_fprint_groups(fprint_groups, **filters)
    if output != lib.OUTPUT_DEFAULT and output != lib.OUTPUT_WIDE:
        tmp_grps = []
        for grps in fprint_groups:
            tmp_grps.extend(grps)
        fprint_groups = spyctl_fprints.fprint_groups_output(tmp_grps)
    else:
        if output == lib.OUTPUT_DEFAULT:
            if policy_coverage:
                fprint_groups = spyctl_fprints.fprint_grp_output_summary(
                    fprint_groups, True, coverage_percentage
                )
            else:
                fprint_groups = spyctl_fprints.fprint_grp_output_summary(
                    fprint_groups
                )
        else:
            if policy_coverage:
                fprint_groups = spyctl_fprints.fprint_grp_output_wide(
                    fprint_groups, True, coverage_percentage
                )
            else:
                fprint_groups = spyctl_fprints.fprint_grp_output_wide(
                    fprint_groups
                )
        output = lib.OUTPUT_RAW
    cli.show(fprint_groups, output)


def get_fingerprints_matching_files(
    orig_fprints, files: List[IO]
) -> List[Dict]:
    rv = []
    for file in files:
        resrc_data = lib.load_resource_file(file)
        filters = lib.selectors_to_filters(resrc_data)
        if len(filters) == 0:
            cli.err_exit(
                f"Unable generate filters for {file.name}. Does it have a"
                " spec field with selectors?"
            )
        rv.extend(
            filt.filter_fingerprints(
                orig_fprints,
                use_context_filters=False,
                suppress_warning=True,
                **filters,
            )
        )
    if not rv:
        cli.try_log("No fingerprints matched input files")
    return rv


def calc_policy_coverage(
    fingerprints: List[Dict], policies: List[Dict] = None
) -> Tuple[List[Dict], float]:
    """Calculates policy coverage from a list of fingerprints

    Args:
        fingerprints (List[Dict]): List of fingerprints to calculate the
            coverage of
        policies (List[Dict], optional): List of policies to calculate
            coverage with. Defaults to None. If None, will download applied
            policies from the Spyderbat Backend.

    Returns:
        Tuple[List[Dict], float]: (List of uncovered fingerprints, coverage
            percentage)
    """
    ctx = cfg.get_current_context()
    if policies is None:
        policies = api.get_policies(*ctx.get_api_data())
    orig_fprint_groups = spyctl_fprints.make_fingerprint_groups(fingerprints)
    total = 0
    for groups in orig_fprint_groups:
        total += len(groups)
    if total == 0:
        cli.err_exit("No fingerprints to calculate coverage of.")
    uncovered_fprints = fingerprints
    for policy in policies:
        filters = lib.selectors_to_filters(policy)
        uncovered_fprints = filt.filter_fingerprints(
            uncovered_fprints,
            use_context_filters=False,
            suppress_warning=True,
            not_matching=True,
            **filters,
        )
    uncovered_fprint_groups = spyctl_fprints.make_fingerprint_groups(
        uncovered_fprints
    )
    uncovered_tot = 0
    for groups in uncovered_fprint_groups:
        uncovered_tot += len(groups)
    coverage = 1 - (uncovered_tot / total)
    return uncovered_fprint_groups, coverage


def __get_latest_timestamp(obj: Dict):
    latest_timestamp = obj.get(lib.METADATA_FIELD, {}).get(
        lib.LATEST_TIMESTAMP_FIELD
    )
    if not latest_timestamp:
        cli.err_exit(
            f"Resource has no {lib.LATEST_TIMESTAMP_FIELD} field in"
            f" its {lib.METADATA_FIELD}"
        )
    return latest_timestamp


def __get_policies_from_option(pol_names_or_uids: List[str]) -> List[Dict]:
    ctx = cfg.get_current_context()
    policies = api.get_policies(*ctx.get_api_data())
    if not policies:
        cli.err_exit("No policies to use as filters.")
    rv = []
    if ALL in pol_names_or_uids:
        rv = policies
    else:
        filtered_pols = {}
        for pol_name_or_uid in pol_names_or_uids:
            pols = filt.filter_obj(
                policies,
                [
                    [lib.METADATA_FIELD, lib.NAME_FIELD],
                    [lib.METADATA_FIELD, lib.METADATA_UID_FIELD],
                ],
                pol_name_or_uid,
            )
            if len(pols) == 0:
                cli.try_log(
                    "Unable to locate policy with name or UID"
                    f" {pol_name_or_uid}",
                    is_warning=True,
                )
                continue
            for policy in pols:
                pol_uid = policy[lib.METADATA_FIELD][lib.METADATA_UID_FIELD]
                filtered_pols[pol_uid] = policy
        rv = list(filtered_pols.values())
    if not policies:
        cli.err_exit("No policies to use as filters.")
    return rv


def get_fingerprints_matching_policies(
    orig_fprints, policies: List[Dict]
) -> List[Dict]:
    rv = []
    for policy in policies:
        filters = lib.selectors_to_filters(policy)
        rv.extend(
            filt.filter_fingerprints(
                orig_fprints,
                use_context_filters=False,
                suppress_warning=True,
                **filters,
            )
        )
    if not rv:
        cli.try_log("No fingerprints matched input files")
    return rv


def handle_get_policies(name_or_id, output, files, st, et, **filters):
    has_matching = filters.pop("has_matching", False)
    file_output = filters.pop("output_to_file", False)
    ctx = cfg.get_current_context()
    if files:
        policies = []
        for file in files:
            resource_data = lib.load_resource_file(file)
            kind = resource_data.get(lib.KIND_FIELD)
            if kind != lib.POL_KIND:
                cli.try_log(
                    f"Input file {file.name} is not a policy.. skipping",
                    is_warning=True,
                )
                continue
            policies.append(resource_data)
    else:
        policies = api.get_policies(*ctx.get_api_data())
    policies = filt.filter_policies(policies, **filters)
    if name_or_id:
        policies = filt.filter_obj(
            policies,
            [
                [lib.METADATA_FIELD, lib.NAME_FIELD],
                [lib.METADATA_FIELD, lib.METADATA_UID_FIELD],
            ],
            name_or_id,
        )
    if file_output:
        for policy in policies:
            out_fn = lib.find_resource_filename(policy, "policy_output")
            if output != lib.OUTPUT_JSON:
                output = lib.OUTPUT_YAML
            out_fn = lib.unique_fn(out_fn, output)
            cli.show(
                policy, output, dest=lib.OUTPUT_DEST_FILE, output_fn=out_fn
            )
    else:
        if has_matching:
            policies, no_match_pols = calculate_has_matching_fprints(
                policies, st, et
            )
        else:
            no_match_pols = []
        if output != lib.OUTPUT_DEFAULT:
            policies = spyctl_policies.policies_output(
                policies + no_match_pols
            )
        else:
            policies = spyctl_policies.policies_summary_output(
                policies, has_matching, no_match_pols
            )
            output = lib.OUTPUT_RAW
        cli.show(
            policies,
            output,
        )


def calculate_has_matching_fprints(
    policies: List[Dict], st, et
) -> Tuple[List[Dict], List[Dict]]:
    has_matching = []
    no_matching = []
    ctx = cfg.get_current_context()
    machines = api.get_machines(*ctx.get_api_data())
    muids = [m["uid"] for m in machines]
    fingerprints = api.get_fingerprints(*ctx.get_api_data(), muids, (st, et))
    for policy in policies:
        filters = lib.selectors_to_filters(policy)
        if filt.filter_fingerprints(
            fingerprints,
            use_context_filters=False,
            suppress_warning=True,
            **filters,
        ):
            has_matching.append(policy)
        else:
            no_matching.append(policy)
    return has_matching, no_matching


def handle_get_processes(name_or_id, st, et, output, **filters):
    ctx = cfg.get_current_context()
    machines = api.get_machines(*ctx.get_api_data())
    clusters = None
    if cfg.CLUSTER_FIELD in filters or cfg.CLUSTER_FIELD in ctx.get_filters():
        clusters = api.get_clusters(*ctx.get_api_data())
    machines = filt.filter_machines(machines, clusters, **filters)
    muids = [m["uid"] for m in machines]
    processes = api.get_processes(*ctx.get_api_data(), muids, (st, et))
    processes = filt.filter_processes(processes, **filters)
    if name_or_id:
        processes = filt.filter_obj(processes, ["name", "id"], name_or_id)
    if output != lib.OUTPUT_DEFAULT:
        processes = spyctl_procs.processes_output(processes)
    cli.show(
        processes,
        output,
        {lib.OUTPUT_DEFAULT: spyctl_procs.processes_output_summary},
    )


def handle_get_connections(name_or_id, st, et, output, **filters):
    ctx = cfg.get_current_context()
    machines = api.get_machines(*ctx.get_api_data())
    clusters = None
    if cfg.CLUSTER_FIELD in filters or cfg.CLUSTER_FIELD in ctx.get_filters():
        clusters = api.get_clusters(*ctx.get_api_data())
    machines = filt.filter_machines(machines, clusters, **filters)
    muids = [m["uid"] for m in machines]
    connections = api.get_connections(*ctx.get_api_data(), muids, (st, et))
    connections = filt.filter_processes(connections, **filters)
    if name_or_id:
        connections = filt.filter_obj(
            connections, ["proc_name", "id"], name_or_id
        )
    if output != lib.OUTPUT_DEFAULT:
        connections = spyctl_conns.connections_output(connections)

    def summary_output(x):
        return spyctl_conns.connections_output_summary(
            x, filters.get("ignore_ips", False)
        )

    cli.show(
        connections,
        output,
        {lib.OUTPUT_DEFAULT: summary_output},
    )
