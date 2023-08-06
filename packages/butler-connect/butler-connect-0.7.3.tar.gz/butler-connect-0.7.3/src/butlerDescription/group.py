class GroupType():
    unDef   = 'undef'
    groupClimate     = 'group_climate'
    groupAnalytics   = 'group_analytics'
    
class GroupOptionType():
    unDef = 'undef'
    forwardingMQTT = 'forwarding_mqtt'
    class buildingHardware():
        unDef = 'undef'
        heating = 'building_hardware_heating'
        cooling = 'building_hardware_cooling'
        ventilation = 'building_hardware_ventilation'
        lighting = 'building_hardware_lighting'
    class agent():
        building = 'agent_building'