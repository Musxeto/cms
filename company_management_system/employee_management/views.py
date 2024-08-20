from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (
    ApplicantSerializer,
    EmployeeBriefSerializer,
    EmployeeSerializer,
    AdminEmployeeSerializer,
    DepartmentSerializer,
    EmployeeRecordSerializer,
    JobPostingSerializer,
    ApplicationSerializer,
    PerformanceReviewSerializer,
    LeaveSerializer,
    PayrollSerializer,
    ComplianceReportSerializer,
)
from .models import (
    Applicant,
    Employee,
    Department,
    EmployeeRecord,
    JobPosting,
    Application,
    PerformanceReview,
    Leave,
    Payroll,
    ComplianceReport,
)
from django.core.files.storage import default_storage

import cohere

co = cohere.Client(settings.COHERE_API_KEY)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_post(request):
    job_data = request.data.get('job')
    if not job_data:
        return Response({"error": "No job data provided"}, status=status.HTTP_400_BAD_REQUEST)

    title = job_data.get('title')
    description = job_data.get('description')
    qualifications = job_data.get('qualifications')
    specifications = job_data.get('specifications')
    location = job_data.get('location')
    job_type = job_data.get('job_type')
    posted_by = job_data.get('posted_by')

    if not all([title, description, qualifications, specifications, location, job_type]):
        return Response({'error': 'All job fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post_response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Create an engaging and professional social media post for a job opening with the following details:\n\nTitle: {title}\nSpecifications: {specifications}\nLocation: {location}\nType: {job_type}\nDescription: {description}\nQualifications: {qualifications}\n\nThe post should be catchy and encourage people to apply give the response with only the post no other thing.",
            max_tokens=300
        )
        post_content = post_response.generations[0].text.strip()
        return Response({'postContent': post_content})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_job_details(request):
    title = request.data.get('title')
    qualifications = request.data.get('qualifications')
    experience = request.data.get('experience')
    
    
    if not title or not qualifications or not experience:
        return Response({'error': 'Title, experience and qualifications are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        description_response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Generate a detailed job description for a job titled: '{title}' with this experience:\n {experience} and these qualifications: {qualifications} - no headings, no qualifications , no other thing labels only the job description in bullets.",
            max_tokens=300
        )
        description = description_response.generations[0].text.strip()

        specifications_response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Generate detailed job specifications for a job titled '{title}' no headings, no qualifications , no other thing labels only the job specifications in bullter.",
            max_tokens=300
        )
        specifications = specifications_response.generations[0].text.strip()

        qualifications_response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Enhance the following qualifications to be written in a professional way: '{qualifications}' no headings or labels only the qualifications.",
            max_tokens=150
        )
        enhanced_qualifications = qualifications_response.generations[0].text.strip()
        
        experience_response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Enhance the following experience to be written in a professional way: '{experience}' no headings or labels only the qualifications.",
            max_tokens=150
        )
        enhanced_experience = experience_response.generations[0].text.strip()
        return Response({
            'description': description,
            'specifications': specifications,
            'qualifications': enhanced_qualifications,
            'experience': enhanced_experience,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdminUser()]
        elif self.action in ["create", "update", "partial_update"]:
            if self.request.user.is_hr_manager or self.request.user.is_superuser:
                return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Employee.objects.all()
        if user.is_hr_manager:
            return Employee.objects.all()
        return Employee.objects.filter(department=user.department)

    def perform_create(self, serializer):
        employee = serializer.save(is_active=True)
        if "profile_image" in self.request.FILES:
            employee.profile_image = self.request.FILES["profile_image"]
            employee.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        if "profile_image" in self.request.FILES:
            instance.profile_image = self.request.FILES["profile_image"]
            instance.save()

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()
        if request.user.is_superuser or request.user.is_hr_manager:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


class AdminEmployeeView(viewsets.ViewSet):
    serializer_class = AdminEmployeeSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        employees = Employee.objects.all()
        serializer = AdminEmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AdminEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            if "profile_image" in request.FILES:
                image = request.FILES["profile_image"]
                employee.profile_image = image
                employee.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_superuser and (request.user.id != employee.id):
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if employee.is_superuser and (request.user.id != employee.id):
            return Response(status=status.HTTP_403_FORBIDDEN)

        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (user.is_authenticated and hasattr(user, "is_hr_manager") and user.is_hr_manager):
            return Department.objects.all()
        if user.is_authenticated:
            return Department.objects.filter(employees=user)
        return Department.objects.none()

    def partial_update(self, request, *args, **kwargs):
        department = self.get_object()
        manager_id = request.data.get("manager")
        if manager_id:
            try:
                manager = Employee.objects.get(id=manager_id)
                department.manager = manager
                department.save()
                serializer = self.get_serializer(department)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response(
                    {"detail": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return super().partial_update(request, *args, **kwargs)

class DepartmentMemberListView(generics.ListAPIView):
    serializer_class = EmployeeBriefSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_employee = self.request.user

        return Employee.objects.filter(department=current_employee.department)


class EmployeeDepartmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = request.user
        if not employee.department:
            return Response(
                {"detail": "No department assigned"}, status=status.HTTP_404_NOT_FOUND
            )
        department = employee.department
        manager = employee.department.manager
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)


class EmployeeRecordViewSet(viewsets.ModelViewSet):
    queryset = EmployeeRecord.objects.all()
    serializer_class = EmployeeRecordSerializer


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer


class ComplianceReportViewSet(viewsets.ModelViewSet):
    queryset = ComplianceReport.objects.all()
    serializer_class = ComplianceReportSerializer

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            if self.request.user.is_hr_manager or self.request.user.is_superuser:
                return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        print("Incoming data:", self.request.data)
        serializer.save(updated_by=self.request.user)
        
    def perform_destroy(self, instance):
        instance.delete()
        
class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        applicant = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'interviewed', 'hired']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        applicant.status = status
        applicant.save()
        serializer = self.get_serializer(applicant)
        return Response(serializer.data)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        
        # Define valid status transitions
        valid_statuses = ['Applied', 'Reviewed', 'Interview Scheduled', 'Offer Extended', 'Hired', 'Rejected']
        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the status and save
        application.status = new_status
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
