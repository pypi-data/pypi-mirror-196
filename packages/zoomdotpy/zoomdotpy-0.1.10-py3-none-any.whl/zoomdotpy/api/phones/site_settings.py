from ..base import _BaseAPI

class SiteSettingsAPI(_BaseAPI):
    def get_site_setting(self, site_id: str, setting_type: str):
        """
            Sites allow you to organize Zoom Phone users in your organization. Use this API to get site setting about a specific [site](https://support.zoom.us/hc/en-us/articles/360020809672) according to the setting type.
			
			**Prerequisites:** 
			
			* Account must have a Pro or a higher plan with Zoom Phone license.
			* Multiple sites must be [enabled](https://support.zoom.us/hc/en-us/articles/360020809672-Managing-Multiple-Sites#h_05c88e35-1593-491f-b1a8-b7139a75dc15).
			
			**Scope:** `phone:read:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        res = self.request(
            'GET',
            f'phone/sites/{site_id}/settings/{setting_type}'
        )

        return res.json()


    def update_site_setting(self, site_id: str, setting_type: str, body: dict) -> bool:
        """
            Sites allow you to organize Zoom Phone users in your organization. Use this API to update the site setting of a specific [site](https://support.zoom.us/hc/en-us/articles/360020809672) according to the setting type.
			
			**Prerequisites:** 
			* Account must have a Pro or a higher plan with Zoom Phone license.
			* Multiple sites must be [enabled](https://support.zoom.us/hc/en-us/articles/360020809672-Managing-Multiple-Sites#h_05c88e35-1593-491f-b1a8-b7139a75dc15).
			
			**Scope:** `phone:write:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        res = self.request(
            'PATCH',
            f'phone/sites/{site_id}/settings/{setting_type}',
            json=body
        )

        if res.status_code == 204:
            return True
        else:
            raise Exception(res.json()['message'])


    def create_site_setting(self, site_id: str, setting_type: str, body: dict):
        """
            Sites allow you to organize Zoom Phone users in your organization. Use this API to add a site setting to a specific [site](https://support.zoom.us/hc/en-us/articles/360020809672) according to the setting type.
			
			**Prerequisites:** 
			* Account must have a Pro or a higher plan with Zoom Phone license.
			* Multiple sites must be [enabled](https://support.zoom.us/hc/en-us/articles/360020809672-Managing-Multiple-Sites#h_05c88e35-1593-491f-b1a8-b7139a75dc15).
			
			**Scope:** `phone:write:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        res = self.request(
            'POST',
            f'phone/sites/{site_id}/settings/{setting_type}',
            json=body
        )

        return res.json()


    def delete_site_setting(self, site_id: str, setting_type: str, params: dict = {}) -> bool:
        """
            Sites allow you to organize Zoom Phone users in your organization. Use this API to delete the site setting of a specific [site](https://support.zoom.us/hc/en-us/articles/360020809672).
			
			**Prerequisites:** 
			* Account must have a Pro or a higher plan with Zoom Phone license.
			* Multiple sites must be [enabled](https://support.zoom.us/hc/en-us/articles/360020809672-Managing-Multiple-Sites#h_05c88e35-1593-491f-b1a8-b7139a75dc15).
			
			**Scope:** `phone:write:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        res = self.request(
            'DELETE',
            f'phone/sites/{site_id}/settings/{setting_type}',
            params=params
        )

        if res.status_code == 204:
            return True
        else:
            raise Exception(res.json()['message'])
    