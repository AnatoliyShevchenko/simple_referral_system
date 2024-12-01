from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from .views import AuthView


class AuthViewTests(APITestCase):
    factory = APIRequestFactory()

    def setUp(self):
        pass

    def test_auth_view_incorrect_post(self):
        """Test Auth View with incorrect phone number."""
        request = self.factory.post(
            path=reverse("auth"), format="json",
            data={"phone_number": "0123456789"}
        )
        response = AuthView.as_view()(request)
        self.assertEqual(
            first=response.status_code, second=status.HTTP_400_BAD_REQUEST
        )

    def test_auth_view_correct(self):
        request = self.factory.post(
            path=reverse("auth"), format="json",
            data={"phone_number": "+77777777777"}
        )
        response = AuthView.as_view()(request)
        self.assertEqual(
            first=response.status_code, second=status.HTTP_200_OK
        )
        code = response.data["message"].removeprefix(
            "Your authenticate code has been sent to your phone! ("
        ).removesuffix(") It's active only for 2 minutes!")
        request = self.factory.patch(
            path=reverse("auth"), format="json",
            data={"auth_code": code}
        )
        response = AuthView.as_view()(request)
        self.assertEqual(
            first=response.status_code, second=status.HTTP_200_OK
        )

    def test_auth_view_incorrect(self):
        request = self.factory.post(
            path=reverse("auth"), format="json",
            data={"phone_number": "+77777777777"}
        )
        response = AuthView.as_view()(request)
        request = self.factory.patch(
            path=reverse("auth"), format="json",
            data={"auth_code": "1123"}
        )
        response = AuthView.as_view()(request)
        self.assertEqual(
            first=response.status_code, second=status.HTTP_404_NOT_FOUND
        )
