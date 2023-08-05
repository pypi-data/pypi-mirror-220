# urls
NODE_MONITORING_URL = "api/v1/nodes/{node_id}/monitor/server-health/?&apikey={api_key}"
NODE_ACTION_URL = "api/v1/nodes/{node_id}/actions/?apikey={api_key}&location=Delhi"


# action types
ENABLE_RECOVERY_MODE = "enable_recovery_mode"
DISABLE_RECOVERY_MODE = "disable_recovery_mode"
REINSTALL = "reinstall"
REBOOT = "reboot"
POWER_ON = "power_on"
POWER_OFF = "power_off"
RENAME = "rename"
UNLOCK_VM = "unlock_vm"
LOCK_VM = "lock_vm"
