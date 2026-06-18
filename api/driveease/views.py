from django.db.models.fields import capfirst
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ContactListModel, Cars
from .serializers import ContactListSerializer
from .forms import ContactListForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import traceback

from .serializers import CarSerializer, FileUploadSerializer

class CarListView(APIView):
    def get(self, request):
        cars = Cars.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

class CarDetailView(APIView):
    def get(self, request, car_id):
        car = Cars.objects.get(car_id=car_id)
        serializer = CarSerializer(car)
        return Response(serializer.data)

class ContactListView(APIView):
  def get(self, request, format=None):
    obj = ContactListModel.objects.all()
    serializer = ContactListSerializer(obj, many=True)
    
    return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class ContactCreateView(APIView):
  def post(self, request):
    form = ContactListForm(request.data)

    if form.is_valid():
      obj = form.save(commit=False)
      obj.save()

      return Response({'status':'created'})
    else:
      return Response({'status':'errors', 'errors': form.errors})
  
  def put(self, request, pk):
    obj = ContactListModel.objects.get(pk=pk)
    form = ContactListForm(request.data, instance=obj)
    form.save()

    return Response({'status': 'updated'})

  def delete(self, request, pk):
    obj = ContactListModel.objects.get(pk=pk)
    obj.delete()

    return Response({'status': 'deleted'})
  
class ContactDetailView(APIView):
  def get(self, request, pk, format=None):
    obj = ContactListModel.objects.get(pk=pk)
    serializer = ContactListSerializer(obj)

    return Response(serializer.data)
  
@method_decorator(csrf_exempt, name='dispatch')
class SubmitToGmail(APIView):
  def post(self, request):
    try:
      form = ContactListForm(request.data)

      if not form.is_valid():
        return Response({
          'status': 'error',
          'message': 'Invalid form data',
          'errors': form.errors
        }, status=status.HTTP_400_BAD_REQUEST)

      # Build context after validation
      context = {
        "contact_id": form.cleaned_data.get('contact_id'),
        "firstname": form.cleaned_data.get('firstname'),
        "lastname": form.cleaned_data.get('lastname'),
        "contact_email": form.cleaned_data.get('contact_email'),
        "contact_number": form.cleaned_data.get('contact_number'),
        "message": form.cleaned_data.get('message'),
      }

      firstname = form.cleaned_data.get('firstname')
      lastname = form.cleaned_data.get('lastname')
      recipient_email = form.cleaned_data.get('contact_email')

      # Subject lines
      subject_inquiry = f"Inquiry from {firstname} {lastname}"
      subject_thankyou = "Thank You for Contacting DriveEase"

      # Render HTML templates
      html_message_inquiry = render_to_string('contact.html', context)
      plain_message_inquiry = strip_tags(html_message_inquiry)

      html_message_thankyou = render_to_string('thankyou.html', context)
      plain_message_thankyou = strip_tags(html_message_thankyou)

      # Internal team recipients
      internal_recipients = [
        'zrephy08@gmail.com',
      ]

      try:
        # Send inquiry email to team
        mail.send_mail(
          subject_inquiry,
          plain_message_inquiry,
          'zrephy08@gmail.com',  # Use proper from email
          internal_recipients,
          html_message=html_message_inquiry,
          fail_silently=False
        )

        # Send thank-you email to inquirer
        mail.send_mail(
          subject_thankyou,
          plain_message_thankyou,
          'DriveEase <zrephy08@gmail.com>',  # Use proper from email
          [recipient_email],
          html_message=html_message_thankyou,
          fail_silently=False
        )

        return Response({'status': 'sent'}, status=status.HTTP_200_OK)

      except Exception as email_error:
        print(f"Email sending error: {email_error}")
        traceback.print_exc()
        return Response({
          'status': 'error',
          'message': 'Failed to send email notifications'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
      print(f"General error in SubmitToGmail: {e}")
      traceback.print_exc()
      return Response({
        'status': 'error',
        'message': 'Internal server error'
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FileUploadSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        upload = serializer.save()

        return Response({
            "id": upload.id,
            "url": upload.file.url
        })