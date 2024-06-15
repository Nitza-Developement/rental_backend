from rental.shared_serializers.serializers import UserProfileSerializer


def poblate_history_list(history_data, logs, model):
    for log_entry in logs:
        history_data.append(
            {
                "action": log_entry.action,
                "model": model,
                "actor": UserProfileSerializer(log_entry.actor).data,
                "timestamp": log_entry.timestamp.timestamp(),
                "changes": log_entry.changes_display_dict,
            }
        )
    history_data.sort(key=lambda x: x["timestamp"], reverse=True)
