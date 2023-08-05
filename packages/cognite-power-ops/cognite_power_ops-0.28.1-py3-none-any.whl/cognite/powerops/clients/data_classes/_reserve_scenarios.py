from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Optional, Union

from cognite.client import data_modeling as dm
from pydantic import Field

from cognite.powerops.clients.data_classes._core import DomainModel, DomainModelApply, InstancesApply, TypeList

if TYPE_CHECKING:
    from cognite.powerops.clients.data_classes._scenario_mappings import ScenarioMappingApply

__all__ = ["ReserveScenario", "ReserveScenarioApply", "ReserveScenarioList"]


class ReserveScenario(DomainModel):
    space: ClassVar[str] = "power-ops"
    auction: Optional[str] = None
    block: Optional[str] = None
    override_mappings: list[str] = Field([], alias="overrideMappings")
    product: Optional[str] = None
    reserve_group: Optional[str] = Field(None, alias="reserveGroup")
    volume: Optional[int] = None


class ReserveScenarioApply(DomainModelApply):
    space: ClassVar[str] = "power-ops"
    auction: Optional[str] = None
    block: Optional[str] = None
    override_mappings: list[Union["ScenarioMappingApply", str]] = Field(default_factory=list, repr=False)
    product: Optional[str] = None
    reserve_group: Optional[str] = None
    volume: Optional[int] = None

    def _to_instances_apply(self, cache: set[str]) -> InstancesApply:
        if self.external_id in cache:
            return InstancesApply([], [])

        sources = []
        source = dm.NodeOrEdgeData(
            source=dm.ContainerId("power-ops", "ReserveScenario"),
            properties={
                "auction": self.auction,
                "block": self.block,
                "product": self.product,
                "reserveGroup": self.reserve_group,
                "volume": self.volume,
            },
        )
        sources.append(source)

        this_node = dm.NodeApply(
            space=self.space,
            external_id=self.external_id,
            existing_version=self.existing_version,
            sources=sources,
        )
        nodes = [this_node]
        edges = []

        for override_mapping in self.override_mappings:
            edge = self._create_override_mapping_edge(override_mapping)
            if edge.external_id not in cache:
                edges.append(edge)
                cache.add(edge.external_id)

            if isinstance(override_mapping, DomainModelApply):
                instances = override_mapping._to_instances_apply(cache)
                nodes.extend(instances.nodes)
                edges.extend(instances.edges)

        return InstancesApply(nodes, edges)

    def _create_override_mapping_edge(self, override_mapping: Union[str, "ScenarioMappingApply"]) -> dm.EdgeApply:
        if isinstance(override_mapping, str):
            end_node_ext_id = override_mapping
        elif isinstance(override_mapping, DomainModelApply):
            end_node_ext_id = override_mapping.external_id
        else:
            raise TypeError(f"Expected str or ScenarioMappingApply, got {type(override_mapping)}")

        return dm.EdgeApply(
            space="power-ops",
            external_id=f"{self.external_id}:{end_node_ext_id}",
            type=dm.DirectRelationReference("power-ops", "ReserveScenario.overrideMappings"),
            start_node=dm.DirectRelationReference(self.space, self.external_id),
            end_node=dm.DirectRelationReference("power-ops", end_node_ext_id),
        )


class ReserveScenarioList(TypeList[ReserveScenario]):
    _NODE = ReserveScenario
