import { DiscoveryDiscoverAssetsRequest } from '../PiecesSDK/core';
import ConnectorSingleton from '../connection/connector_singleton';
import Notifications from '../connection/notification_handler';
import Constants from '../const';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';

export default async function discoverSnippets(
    params: DiscoveryDiscoverAssetsRequest
) {
    SegmentAnalytics.track({
        event: AnalyticsEnum.JUPYTER_SNIPPET_DISCOVERY,
    });

    const notifications = Notifications.getInstance();
    const config = ConnectorSingleton.getInstance();
    try {
        const result = await config.DiscoveryApi.discoveryDiscoverAssets(
            params
        );

        if (result.iterable.length === 0) {
            notifications.error({
                message: `Something went wrong, we weren't able to find any snippets to discover`,
            });
            return result;
        }

        notifications.information({
            message:
                Constants.DISCOVERY_SUCCESS +
                ` ${result.iterable.length} snippets saved to Pieces!`,
        });
        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_SNIPPET_DISCOVERY_SUCCESS,
        });
        return result;
    } catch (e) {
        notifications.error({ message: Constants.DISCOVERY_FAILURE });
        SegmentAnalytics.track({
            event: AnalyticsEnum.JUPYTER_SNIPPET_DISCOVERY_FAILURE,
        });
    }
}
