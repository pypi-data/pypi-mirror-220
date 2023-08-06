import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_with_relations_cwl_job_inputs import WorkflowWithRelationsCwlJobInputs
    from ..models.workflow_with_relations_inputs import WorkflowWithRelationsInputs
    from ..models.workflow_with_relations_outputs import WorkflowWithRelationsOutputs
    from ..models.workflow_with_relations_steps import WorkflowWithRelationsSteps


T = TypeVar("T", bound="WorkflowWithRelations")


@attr.s(auto_attribs=True)
class WorkflowWithRelations:
    """(tsType: WorkflowWithRelations, schemaOptions: { includeRelations: true })

    Attributes:
        name (str):
        inputs (WorkflowWithRelationsInputs):
        outputs (WorkflowWithRelationsOutputs):
        steps (WorkflowWithRelationsSteps):
        cwl_job_inputs (WorkflowWithRelationsCwlJobInputs):
        id (Union[Unset, str]):
        driver (Union[Unset, str]):
        status (Union[Unset, str]):
        date_created (Union[Unset, datetime.datetime]):
        date_finished (Union[Unset, datetime.datetime]):
        owner (Union[Unset, str]):
    """

    name: str
    inputs: "WorkflowWithRelationsInputs"
    outputs: "WorkflowWithRelationsOutputs"
    steps: "WorkflowWithRelationsSteps"
    cwl_job_inputs: "WorkflowWithRelationsCwlJobInputs"
    id: Union[Unset, str] = UNSET
    driver: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    date_finished: Union[Unset, datetime.datetime] = UNSET
    owner: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        inputs = self.inputs.to_dict()

        outputs = self.outputs.to_dict()

        steps = self.steps.to_dict()

        cwl_job_inputs = self.cwl_job_inputs.to_dict()

        id = self.id
        driver = self.driver
        status = self.status
        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        date_finished: Union[Unset, str] = UNSET
        if not isinstance(self.date_finished, Unset):
            date_finished = self.date_finished.isoformat()

        owner = self.owner

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "inputs": inputs,
                "outputs": outputs,
                "steps": steps,
                "cwlJobInputs": cwl_job_inputs,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if driver is not UNSET:
            field_dict["driver"] = driver
        if status is not UNSET:
            field_dict["status"] = status
        if date_created is not UNSET:
            field_dict["dateCreated"] = date_created
        if date_finished is not UNSET:
            field_dict["dateFinished"] = date_finished
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_with_relations_cwl_job_inputs import WorkflowWithRelationsCwlJobInputs
        from ..models.workflow_with_relations_inputs import WorkflowWithRelationsInputs
        from ..models.workflow_with_relations_outputs import WorkflowWithRelationsOutputs
        from ..models.workflow_with_relations_steps import WorkflowWithRelationsSteps

        d = src_dict.copy()
        name = d.pop("name")

        inputs = WorkflowWithRelationsInputs.from_dict(d.pop("inputs"))

        outputs = WorkflowWithRelationsOutputs.from_dict(d.pop("outputs"))

        steps = WorkflowWithRelationsSteps.from_dict(d.pop("steps"))

        cwl_job_inputs = WorkflowWithRelationsCwlJobInputs.from_dict(d.pop("cwlJobInputs"))

        id = d.pop("id", UNSET)

        driver = d.pop("driver", UNSET)

        status = d.pop("status", UNSET)

        _date_created = d.pop("dateCreated", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _date_finished = d.pop("dateFinished", UNSET)
        date_finished: Union[Unset, datetime.datetime]
        if isinstance(_date_finished, Unset):
            date_finished = UNSET
        else:
            date_finished = isoparse(_date_finished)

        owner = d.pop("owner", UNSET)

        workflow_with_relations = cls(
            name=name,
            inputs=inputs,
            outputs=outputs,
            steps=steps,
            cwl_job_inputs=cwl_job_inputs,
            id=id,
            driver=driver,
            status=status,
            date_created=date_created,
            date_finished=date_finished,
            owner=owner,
        )

        workflow_with_relations.additional_properties = d
        return workflow_with_relations

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
