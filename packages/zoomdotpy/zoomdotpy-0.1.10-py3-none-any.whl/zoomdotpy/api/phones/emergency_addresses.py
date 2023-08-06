from ..base import _BaseAPI

class EmergencyAddressesAPI(_BaseAPI):
    def list_emergency_addresses(self, params: dict):
        """
            Lists the emergency addresses.
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        res = self.request(
            'GET',
            f'phone/emergency_addresses',
            params=params
        )

        return res.json()


    def create_emergency_address(self, body: dict):
        """
            Adds an emergency address. If the address provided is not an exact match, the system generated corrected address will be used. 
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        res = self.request(
            'POST',
            f'phone/emergency_addresses',
            json=body
        )

        return res.json()
    

    def delete_emergency_address(self, emergency_address_id: str):
        """
            Removes an emergency address.
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Heavy`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        res = self.request(
            'DELETE',
            f'phone/emergency_addresses/{emergency_address_id}'
        )

        return res.json()


    def get_emergency_address(self, emergency_address_id: str):
        """
            Gets the emergency address information.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions<br>
        """

        res = self.request(
            'GET',
            f'phone/emergency_addresses/{emergency_address_id}'
        )

        return res.json()


    def update_emergency_address(self, emergency_address_id: str, body: dict) -> bool:
        """
            Updates an emergency address information. If the address provided is not an exact match, the system generated corrected address will be used. 
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        res = self.request(
            'PATCH',
            f'phone/emergency_addresses/{emergency_address_id}',
            json=body
        )

        return res.status_code == 204