resources_with_submitted_status = [
    resource_detail["resource"]
    for item in response["value"]
    if item["status"] == "submitted"
    for resource_detail in item["resourceDetails"]
]
