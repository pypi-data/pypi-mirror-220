import asyncio
import os
from aiodatastore import (
    Entity,
    KindExpression,
    BooleanValue,
    Datastore,
    Query,
    PartitionId,
    PropertyFilter,
    PropertyReference,
    PropertyFilterOperator,
    Key,
    PathElement,
    StringValue,
    IntegerValue,
    NullValue,
)


VALUE = {
    "key": {
        "partitionId": {"projectId": "kitchenhub-app-prod", "namespaceId": ""},
        "path": [{"kind": "Restaurant", "id": "6014272099057664"}],
    },
    "properties": {
        "churn_at": {
            "excludeFromIndexes": False,
            "timestampValue": "2021-08-23T09:36:44.714724000Z",
        },
        "restaurant_email": {
            "excludeFromIndexes": False,
            "stringValue": "tbec-toastys@trivreats.com",
        },
        "print_modifier_on_front_receipt": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "subscription_status": {
            "excludeFromIndexes": False,
            "stringValue": "paid",
        },
        "restaurant_delivery_time": {
            "excludeFromIndexes": False,
            "integerValue": 145,
        },
        "restaurant_id": {
            "excludeFromIndexes": False,
            "stringValue": "30e6bbbc-2a55-4ee0-bfcf-3d6d31bfce05",
        },
        "proxy_restaurant": {
            "excludeFromIndexes": False,
            "booleanValue": True,
        },
        "print_receipt_number": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "auto_accept_cooking_time": {
            "excludeFromIndexes": False,
            "integerValue": 20,
        },
        "split_kitchen_receipt": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "user_id": {
            "excludeFromIndexes": False,
            "arrayValue": {
                "values": [
                    {
                        "excludeFromIndexes": False,
                        "stringValue": "dc066810-1e7b-4e7c-aa80-2f70c40313fc",
                    },
                    {
                        "excludeFromIndexes": False,
                        "stringValue": "e9ce44e0-b421-430c-9b3b-02f61055f53d",
                    },
                    {
                        "excludeFromIndexes": False,
                        "stringValue": "c930f030-8e17-41e0-8ecf-c0acdab09b69",
                    },
                ]
            },
        },
        "show_option_modifier": {
            "excludeFromIndexes": False,
            "booleanValue": True,
        },
        "website_orders_confirm_sms_text": {
            "excludeFromIndexes": False,
            "nullValue": "NULL_VALUE",
        },
        "restaurant_state": {"excludeFromIndexes": False, "stringValue": "WA"},
        "restaurant_phone_number": {
            "excludeFromIndexes": False,
            "nullValue": "NULL_VALUE",
        },
        "paid_at": {
            "excludeFromIndexes": False,
            "timestampValue": "2021-12-19T18:35:37.795724000Z",
        },
        "tablet_model": {
            "excludeFromIndexes": False,
            "stringValue": "TB-X606F",
        },
        "restaurant_lat": {
            "excludeFromIndexes": False,
            "doubleValue": 47.63458,
        },
        "front_receipt_footer_text": {
            "excludeFromIndexes": False,
            "stringValue": "",
        },
        "has_printer": {"excludeFromIndexes": False, "booleanValue": True},
        "print_recipe_on_kitchen_receipt": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "restaurant_name": {
            "excludeFromIndexes": False,
            "stringValue": "The Brief Encounter Cafe",
        },
        "updated_by": {
            "excludeFromIndexes": False,
            "stringValue": "dc066810-1e7b-4e7c-aa80-2f70c40313fc",
        },
        "updated_at": {
            "excludeFromIndexes": False,
            "timestampValue": "2022-11-12T22:55:46.375083000Z",
        },
        "ask_for_delivery_by_postmates": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "play_new_order_sound": {
            "excludeFromIndexes": False,
            "booleanValue": True,
        },
        "paid_set_by": {
            "excludeFromIndexes": False,
            "stringValue": "56757361-25f0-4c8f-a583-a358b007a411",
        },
        "send_confirm_sms_for_website_orders": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "tablet_manufacturer": {
            "excludeFromIndexes": False,
            "stringValue": "Lenovo",
        },
        "restaurant_timezone": {
            "excludeFromIndexes": False,
            "stringValue": "America/Los_Angeles",
        },
        "restaurant_zip": {
            "excludeFromIndexes": False,
            "stringValue": "98004",
        },
        "created_at": {
            "excludeFromIndexes": False,
            "timestampValue": "2021-02-19T17:30:16.714751000Z",
        },
        "restaurant_street": {
            "excludeFromIndexes": False,
            "stringValue": "2632 Bellevue Way NE",
        },
        "subscription_plan": {
            "excludeFromIndexes": False,
            "stringValue": "aggregation",
        },
        "restaurant_city": {
            "excludeFromIndexes": False,
            "stringValue": "Bellevue",
        },
        "pos_enabled": {"excludeFromIndexes": False, "booleanValue": False},
        "virtual_brand_company_id": {
            "excludeFromIndexes": False,
            "stringValue": "TRIVREATS",
        },
        "paid_reason": {
            "excludeFromIndexes": False,
            "nullValue": "NULL_VALUE",
        },
        "restaurant_lon": {
            "excludeFromIndexes": False,
            "doubleValue": -122.20069,
        },
        "print_modifier_on_kitchen_receipt": {
            "excludeFromIndexes": False,
            "booleanValue": False,
        },
        "restaurant_website": {"excludeFromIndexes": False, "stringValue": ""},
        "auto_accept_enabled": {
            "excludeFromIndexes": False,
            "booleanValue": True,
        },
        "trial_period_days": {"excludeFromIndexes": False, "integerValue": 14},
        "proxy_restaurant_id": {
            "excludeFromIndexes": False,
            "nullValue": "NULL_VALUE",
        },
        "show_new_order_notification": {
            "excludeFromIndexes": False,
            "booleanValue": True,
        },
    },
}


async def main():
    ds = Datastore(
        project_id="kitchenhub-app-sandbox",
        service_file=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
    )

    # query = Query(
    #     kind=KindExpression('MyEntity'),
    #     # filter=PropertyFilter(
    #     #     property=PropertyReference("integer-field"),
    #     #     op=PropertyFilterOperator.EQUAL,
    #     #     value=IntegerValue(value=456),
    #     # ),
    # )
    # result = await ds.run_query(query)
    # for er in result.entity_results:
    #     print(er.entity.to_ds())
    # entity = result.entity_results[0].entity
    # print(entity.to_ds())

    # cr = await ds.delete(key=entity.key)
    # print("delete result", cr)

    entity = Entity(
        key=Key(
            partition_id=PartitionId(project_id="kitchenhub-app-sandbox"),
            path=[PathElement("MyEntity")],
        ),
        properties={
            "integer-field": IntegerValue(123),
            "string-field": StringValue("123"),
        },
    )
    # entity.properties = {
    #     "null2-value": NullValue(),
    # }
    await ds.insert(entity)

    # key1 = Key(
    #     partition_id=PartitionId(project_id="kitchenhub-app-sandbox"),
    #     path=[PathElement("MyEntity")],
    # )
    # key2 = Key(
    #     partition_id=PartitionId(project_id="kitchenhub-app-sandbox"),
    #     path=[PathElement("MyEntity")],
    # )
    # keys = await ds.allocate_ids(keys=[key1, key2])
    # await ds.reserve_ids(keys=keys)
    await ds.close()


if __name__ == "__main__":
    asyncio.run(main())
