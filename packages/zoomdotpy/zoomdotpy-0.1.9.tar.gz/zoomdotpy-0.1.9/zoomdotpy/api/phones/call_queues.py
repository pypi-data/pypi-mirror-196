from ..base import _BaseAPI

class CallQueuesAPI(_BaseAPI):
    def list_call_queues(self, params: dict = {}):
        """
            Call queues allow you to route incoming calls to a group of users. For instance, you can use call queues to route calls to various departments in your organization such as sales, engineering, billing, customer service etc.
			 Use this API to list Call queues.
			
			
			**Prerequisites:**
			
			* Pro, Business, or Education account
			* Account owner or admin permissions
			* Zoom Phone license
			
			**Scopes:** `phone:read:admin`
			 
			
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
			
        """

        res = self.request(
            'GET',
            f'phone/call_queues',
            params=params
        )

        return res.json()

    def create_call_queue(self, body: dict):
        """
            Call queues allow you to route incoming calls to a group of users. For instance, you can use call queues to route calls to various departments in your organization such as sales, engineering, billing, customer service etc.
			 Use this API to [create a call queue](https://support.zoom.us/hc/en-us/articles/360021524831-Managing-Call-Queues#h_e81faeeb-9184-429a-aaea-df49ff5ff413).
			 You can add phone users or common area phones to call queues.
			
			**Prerequisites:**
			
			* Pro, Business, or Education account
			* Account owner or admin permissions
			* Zoom Phone license
			
			**Scopes:** `phone:write:admin`
			 
			
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        res = self.request(
            'POST',
            f'phone/call_queues',
            json=body
        )

        return res.json()
    
    def delete_call_queue(self, call_queue_id: str) -> bool:
        """
            Call queues allow you to route incoming calls to a group of users. For instance, you can use call queues to route calls to various departments in your organization such as sales, engineering, billing, customer service etc.
			 Use this API to delete a Call Queue.
			 
			**Prerequisites:**
			
			* Pro, Business, or Education account
			* Account owner or admin permissions
			* Zoom Phone license
			
			**Scopes:** `phone:write:admin`
			 
			
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			
        """


        res = self.request(
            'DELETE',
            f'phone/call_queues/{call_queue_id}'
        )

        if res.status_code == 204:
            return True
        else:
            raise Exception(res.json()['message'])

    def get_call_queue(self, call_queue_id: str):
        """
            Call queues allow you to route incoming calls to a group of users. For instance, you can use call queues to route calls to various departments in your organization such as sales, engineering, billing, customer service etc.
			 Use this API to get information on a specific Call Queue.
			
			 
			**Prerequisites:**
			
			* Pro, Business, or Education account
			* Account owner or admin permissions
			* Zoom Phone license
			
			**Scopes:** `phone:read:admin`
			 
			
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """


        res = self.request(
            'GET',
            f'phone/call_queues/{call_queue_id}'
        )

        return res.json()

    def update_call_queue(self, call_queue_id: str, body: dict) -> bool:
        """
            Call queues allow you to route incoming calls to a group of users. For instance, you can use call queues to route calls to various departments in your organization such as sales, engineering, billing, customer service etc.
			 Use this API to update information of a specific Call Queue.
			 
			**Prerequisites:**
			
			* Pro, Business, or Education account
			* Account owner or admin permissions
			* Zoom Phone license
			
			**Scopes:** `phone:write:admin`
			 
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
        """


        res = self.request(
            'PATCH',
            f'phone/call_queues/{call_queue_id}',
            json=body
        )

        if res.status_code == 204:
            return True
        else:
            raise Exception(res.json()['message'])