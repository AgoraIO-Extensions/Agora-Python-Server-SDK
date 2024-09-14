"""
RTCConnectionObserver
conn_info: instantce of RTCConnInfo
agora_rtc_conn: instance of RTCConnection
reasion: int type of error code
quality: ref to c++ sdk
"""
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
    #error:int, api_type/api_param:string
    def on_api_call_executed(self, agora_rtc_conn, error, api_type, api_param):
        pass

    #result: int
    def on_content_inspect_result(self, agora_rtc_conn, result):
        pass

    #uid: int, file_path: str, width: int, height: int, err_code: int
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