import json
import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import IndustryType, Employer, Jobseeker
from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience
from recruitsite import settings

JSON_PATH = os.path.join(settings.BASE_DIR, 'db_json')


def load_dbjson(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding="UTF-8") as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):

        IndustryType.objects.all().delete()

        types_ = [
            'IT',
            'Банковские услуги',
            'Маркетинг',
            'Бухгалтерия'
        ]
        ind = 0
        for type_ in types_:
            ind += 1
            IndustryType.objects.create(id=ind, descx=type_)

        # User.objects.get(username='django').delete()
        User.objects.all().delete()
        User.objects.create_superuser('django', 'django@superuser.local', 'test123')

        employers = load_dbjson('employers')

        for employer in employers:
            user = User.objects.create_user(employer['username'], employer['email'], employer['password'])
            Employer.objects.create(user_id=user.id, **employer['data'])

        jobseekers = load_dbjson('jobseekers')

        for jobseeker in jobseekers:
            user = User.objects.create_user(username=jobseeker['username'], email=jobseeker['email'], password=jobseeker['password'],
                                            first_name=jobseeker['first_name'], last_name=jobseeker['last_name'])
            Jobseeker.objects.create(user_id=user.id, **jobseeker['data'])

            if 'resumes' in jobseeker:
                for resume_ in jobseeker['resumes']:
                    object = Resume.objects.create(user_id=user.id, **resume_['main_info'])
                    if 'education' in resume_:
                        for education in resume_['education']:
                            ResumeEducation.objects.create(resume_id=object.id, **education)
                    if 'experience' in resume_:
                        for experience in resume_['experience']:
                            ResumeExperience.objects.create(resume_id=object.id, **experience)
