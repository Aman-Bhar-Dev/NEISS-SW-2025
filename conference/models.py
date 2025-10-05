from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# -------------------------------
# USER PROFILE (for phone & institute)
# -------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    institute = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# -------------------------------
# AbstractSubmission & CoAuthor
# -------------------------------
class AbstractSubmission(models.Model):
    main_author = models.CharField(max_length=255)
    email = models.EmailField()
    abstract_file = models.FileField(upload_to='abstracts/', storage=RawMediaCloudinaryStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    paper_id = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    INSTITUTE_CHOICES = [
        ('Assam University, Silchar', 'Assam University, Silchar'),
        ('Others', 'Others'),
    ]
    institute = models.CharField(max_length=100, choices=INSTITUTE_CHOICES)
    custom_institute = models.CharField(max_length=255, blank=True, null=True)

    DESIGNATION_CHOICES = [
        ('Student', 'Student'),
        ('Research Scholar', 'Research Scholar'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
    ]
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)

    ACCOMMODATION_CHOICES = [('REQUIRED', 'REQUIRED'), ('NOT-REQUIRED', 'NOT REQUIRED')]
    ACCOMMODATION = models.CharField(max_length=20, choices=ACCOMMODATION_CHOICES, default='NOT-REQUIRED')
    

    FOOD_PREFERENCE_CHOICES = [('NON-VEG', 'VEG'), ('NON-VEG', 'VEG')]
    FOOD_PREFERENCE = models.CharField(max_length=20, choices=FOOD_PREFERENCE_CHOICES, default='VEG')
    

    keywords = models.TextField()
    full_paper = models.FileField(
        upload_to='full_papers/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage()
    )

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_on = models.DateTimeField(auto_now_add=True)

    payment_amount = models.IntegerField(default=0)
    payment_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.paper_id:
            last = AbstractSubmission.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.paper_id = f"NEISS{10000 + next_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.paper_id} - {self.title}"

    # Co-author helper methods (name, email, designation, affiliation, accommodation, food preference)
    def _get_full_name(self, index):
        coauthors = list(self.coauthors.all())
        if len(coauthors) > index:
            return f"{coauthors[index].first_name} {coauthors[index].last_name}"
        return ''

    def _get_coauthor_attr(self, index, attr):
        coauthors = list(self.coauthors.all())
        if len(coauthors) > index:
            return getattr(coauthors[index], attr, '')
        return ''

    # Example for 5 co-authors
    def get_coauthor1_name(self): return self._get_full_name(0)
    def get_coauthor1_email(self): return self._get_coauthor_attr(0, 'email')
    def get_coauthor1_designation(self): return self._get_coauthor_attr(0, 'designation')
    def get_coauthor1_affiliation(self): return self._get_coauthor_attr(0, 'affiliation')
    def get_coauthor1_accommodation(self): return self._get_coauthor_attr(0, 'ACCOMMODATION')
    def get_coauthor1_food(self): return self._get_coauthor_attr(0, 'FOOD_PREFERENCE')

    def get_coauthor2_name(self): return self._get_full_name(1)
    def get_coauthor2_email(self): return self._get_coauthor_attr(1, 'email')
    def get_coauthor2_designation(self): return self._get_coauthor_attr(1, 'designation')
    def get_coauthor2_affiliation(self): return self._get_coauthor_attr(1, 'affiliation')
    def get_coauthor2_accommodation(self): return self._get_coauthor_attr(1, 'ACCOMMODATION')
    def get_coauthor2_food(self): return self._get_coauthor_attr(1, 'FOOD_PREFERENCE')

    def get_coauthor3_name(self): return self._get_full_name(2)
    def get_coauthor3_email(self): return self._get_coauthor_attr(2, 'email')
    def get_coauthor3_designation(self): return self._get_coauthor_attr(2, 'designation')
    def get_coauthor3_affiliation(self): return self._get_coauthor_attr(2, 'affiliation')
    def get_coauthor3_accommodation(self): return self._get_coauthor_attr(2, 'ACCOMMODATION')
    def get_coauthor3_food(self): return self._get_coauthor_attr(2, 'FOOD_PREFERENCE')

    def get_coauthor4_name(self): return self._get_full_name(3)
    def get_coauthor4_email(self): return self._get_coauthor_attr(3, 'email')
    def get_coauthor4_designation(self): return self._get_coauthor_attr(3, 'designation')
    def get_coauthor4_affiliation(self): return self._get_coauthor_attr(3, 'affiliation')
    def get_coauthor4_accommodation(self): return self._get_coauthor_attr(3, 'ACCOMMODATION')
    def get_coauthor4_food(self): return self._get_coauthor_attr(3, 'FOOD_PREFERENCE')

    def get_coauthor5_name(self): return self._get_full_name(4)
    def get_coauthor5_email(self): return self._get_coauthor_attr(4, 'email')
    def get_coauthor5_designation(self): return self._get_coauthor_attr(4, 'designation')
    def get_coauthor5_affiliation(self): return self._get_coauthor_attr(4, 'affiliation')
    def get_coauthor5_accommodation(self): return self._get_coauthor_attr(4, 'ACCOMMODATION')
    def get_coauthor5_food(self): return self._get_coauthor_attr(4, 'FOOD_PREFERENCE')


class CoAuthor(models.Model):
    submission = models.ForeignKey(AbstractSubmission, on_delete=models.CASCADE, related_name='coauthors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    affiliation = models.CharField(max_length=200)

    DESIGNATION_CHOICES = [
        ('Student', 'Student'),
        ('Research Scholar', 'Research Scholar'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
    ]
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)

    ACCOMMODATION_CHOICES = [('REQUIRED', 'REQUIRED'), ('NOT-REQUIRED', 'NOT-REQUIRED')]
    ACCOMMODATION = models.CharField(max_length=20, choices=ACCOMMODATION_CHOICES,default='NOT-REQUIRED')
    

    FOOD_PREFERENCE_CHOICES = [('NON-VEG', 'VEG'), ('NON-VEG', 'VEG')]
    FOOD_PREFERENCE = models.CharField(max_length=20, choices=FOOD_PREFERENCE_CHOICES,default='VEG')
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']



#----- Payment related --------#

from django.db import models
from .models import AbstractSubmission  # adjust if needed
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class FinalRegistration(models.Model):

    THEME_CHOICES = [
        ('Society, Equity, Transformation & Social Work', 'Society, Equity, Transformation & Social Work'),
        ('Knowledge, Education & Human Development', 'Knowledge, Education & Human Development'),
        ('Politics, Governance, Public Policy, and Political Science', 'Politics, Governance, Public Policy, and Political Science'),
        ('Economy, Technology & Social Impact', 'Economy, Technology & Social Impact'),
        ('Culture, Identity & Globalization', 'Culture, Identity & Globalization'),
        ('Environment, Climate & Sustainability', 'Environment, Climate & Sustainability'),
        ('Business, Commerce and Business Sustainability', 'Business, Commerce and Business Sustainability'),
        ('General Social Science and Topics Not Falling Under the Above Categories', 'General Social Science and Topics Not Falling Under the Above Categories'),
    ]

    submission = models.OneToOneField(AbstractSubmission, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255)
    author_designation = models.CharField(max_length=100)
    author_contact = models.CharField(max_length=20)
    author_gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    author_address = models.TextField()
    author_mode = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    author_id_proof = models.FileField(upload_to='id_proofs/',storage=RawMediaCloudinaryStorage())
    total_amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    presenter_name = models.CharField(max_length=255, blank=True, null=True)
    fee_breakdown = models.TextField(blank=True)
    transaction_date = models.DateField(blank=True, null=True)
    transaction_time = models.TimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    selected_theme = models.CharField(
        max_length=200,
        choices=THEME_CHOICES,
        blank=True,
        null=True
    )
    payment_verified = models.BooleanField(default=False)

    # 🔽 Payment screenshot upload (Cloudinary)
    payment_screenshot = models.ImageField(
        upload_to='payment_screenshots/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage()
    )

    def __str__(self):
        return f"{self.submission.paper_id} - Final Registration"

    # ✅ Admin helper method
    def has_paid(self):
        return bool(self.transaction_id and self.payment_screenshot)

    has_paid.boolean = True
    has_paid.short_description = "Payment Done?"
class FinalParticipant(models.Model):
    registration = models.ForeignKey(FinalRegistration, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)  # Email for co-authors only
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    role = models.CharField(max_length=20, choices=[('CoAuthor', 'Co-Author'), ('Visitor', 'Visitor')])
    mode = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True, storage=RawMediaCloudinaryStorage())
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.role})"
    
# conference/models.py

from django.db import models

ID_PROOF_CHOICES = [
    ('passport', 'Passport'),
    ('voter_id', 'Voter ID'),
]

STATUS_CHOICES = [
    ('Pending',  'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class VisitorRegistration(models.Model):
    name           = models.CharField(max_length=100)
    email          = models.EmailField()
    contact        = models.CharField(max_length=15)
    address        = models.TextField()
    id_proof_type  = models.CharField(max_length=20, choices=ID_PROOF_CHOICES)
    id_proof_file  = models.FileField(upload_to='identity_proofs/',storage=RawMediaCloudinaryStorage())
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    timestamp      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class AdditionalVisitor(models.Model):
    group = models.ForeignKey(VisitorRegistration, on_delete=models.CASCADE, related_name='additional_visitors')
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    id_proof_type = models.CharField(max_length=20, choices=ID_PROOF_CHOICES)
    id_proof_file = models.FileField(upload_to='identity_proofs/')

    def __str__(self):
        return f"{self.name} ({self.contact})"
