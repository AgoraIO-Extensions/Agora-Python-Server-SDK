class IRTCConnectionObserver():
    def on_connected(self, agora_rtc_conn, conn_info, reason):
        pass

    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        pass

    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        pass

    def on_reconnecting(self, agora_rtc_conn, conn_info, reason):
        pass

    def on_reconnected(self, agora_rtc_conn, conn_info, reason):
        pass

    def on_connection_lost(self, agora_rtc_conn, conn_info):
        pass

    def on_lastmile_quality(self, agora_rtc_conn, quality):
        pass

    def on_lastmile_probe_result(self, agora_rtc_conn, result):
        pass

    def on_token_privilege_will_expire(self, agora_rtc_conn, token):
        pass

    def on_token_privilege_did_expire(self, agora_rtc_conn):
        pass

    def on_connection_license_validation_failure(self, agora_rtc_conn, reason):
        pass

    def on_connection_failure(self, agora_rtc_conn, info, reason):
        pass

    def on_user_joined(self, agora_rtc_conn, user_id):
        pass

    def on_user_left(self, agora_rtc_conn, user_id, reason):
        pass

    def on_transport_stats(self, agora_rtc_conn, stats):
        pass

    def on_change_role_success(self, agora_rtc_conn, old_role, new_role):
        pass

    def on_change_role_failure(self, agora_rtc_conn, reason, cur_role):
        pass

    def on_user_network_quality(self, agora_rtc_conn, uid, tx_quality, rx_quality):
        pass

    def on_network_type_changed(self, agora_rtc_conn, network_type):
        pass

    def on_api_call_executed(self, agora_rtc_conn, error, api_type, api_param):
        pass

    def on_content_inspect_result(self, agora_rtc_conn, result):
        pass

    def on_snapshot_taken(self, agora_rtc_conn, uid, file_path, width, height, err_code):
        pass

    def on_error(self, agora_rtc_conn, error_code, error_msg):
        pass

    def on_warning(self, agora_rtc_conn, warn_code, warn_msg):
        pass

    def on_channel_media_relay_state_changed(self, agora_rtc_conn, state, code):
        pass

    def on_local_user_registered(self, agora_rtc_conn, uid, user_account):
        pass

    def on_user_account_updated(self, agora_rtc_conn, uid, user_account):
        pass

    def on_stream_message_error(self, agora_rtc_conn, user_id_str, stream_id, code, missed, cached):
        pass

    def on_encryption_error(self, agora_rtc_conn, error_type):
        pass

    def on_upload_log_result(self, agora_rtc_conn, request_id_str, success, reason):
        pass
    def on_encryption_error(self, agora_rtc_conn, error_type: int):
        pass
    def on_aiqos_capability_missing(self, agora_rtc_conn, recommend_audio_scenario)->int:
        """
            //date: 2025-06-27
        // Triggered when the following two conditions are both met:
        // 1. The developer sets the connection's scenario to AudioScenarioAiServer.
        // 2. The version of the SDK on the client side does not support aiqos.
        // If triggered, it means the client-side version does not support aiqos, and the developer needs to decide to reset the server-side scenario.
        // How should the developer handle it when the callback is triggered?
        // 1. If set return value to -1, it means the SDK internally does not handle the scenario incompatibility.
        // 2. If set return value to a valid scenario, it means the SDK internally automatically falls back to the scenario returned, ensuring compatibility.
        // how to use it: can ref to examples/ai_send_recv_pcm/ai_send_recv_pcm.go

       @parameters:
       agora_rtc_conn: the connection object
       recommend_audio_scenario: the recommended audio scenario
       @return:
       -1: the SDK internally does not handle the scenario incompatibility.
       a valid scenario: the SDK internally automatically falls back to the scenario returned, ensuring compatibility.
        """
        pass