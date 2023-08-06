from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .channel_stop_types import ChannelStopType
from .sales_channels import SalesChannel

__all__ = (
    'StopSale',
    'StopSaleByProduct',
    'StopSaleByIngredient',
    'StopSaleBySalesChannel',
    'StopSaleBySector',
)


class StopSale(BaseModel):
    id: UUID
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    started_at: datetime = Field(alias='startedAt')
    ended_at: datetime | None = Field(alias='endedAt')
    stopped_by_user_id: UUID = Field(alias='stoppedByUserId')
    resumed_by_user_id: UUID | None = Field(alias='resumedByUserId')

    class Config:
        allow_population_by_field_name = True


class StopSaleBySalesChannel(StopSale):
    reason: str
    sales_channel_name: SalesChannel = Field(alias='salesChannelName')
    channel_stop_type: ChannelStopType = Field(alias='channelStopType')


class StopSaleByIngredient(StopSale):
    reason: str
    ingredient_name: str = Field(alias='ingredientName')


class StopSaleByProduct(StopSale):
    reason: str
    product_name: str = Field(alias='productName')


class StopSaleBySector(StopSale):
    sector_name: str = Field(alias='sectorName')
    is_sub_sector: bool = Field(alias='isSubSector')
    stopped_by_user_id: UUID = Field(alias='suspendedByUserId')
    resumed_by_user_id: UUID | None = Field(alias='resumedUserId')
