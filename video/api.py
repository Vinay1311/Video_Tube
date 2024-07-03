# ---------------- External Imports -----------------#
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
# ---------------- Internal Imports -----------------#
from helper import messages, keys