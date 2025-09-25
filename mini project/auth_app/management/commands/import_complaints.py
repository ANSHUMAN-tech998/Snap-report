import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup
from auth_app.models import Complaint
from django.conf import settings
import shutil
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Import complaints from the old HTML file to the database'

    def handle(self, *args, **options):
        # Path to the old index.html file
        html_file = os.path.join(settings.BASE_DIR, 'index.html')
        
        # Create complaints directory if it doesn't exist
        complaints_dir = os.path.join(settings.MEDIA_ROOT, 'complaints')
        os.makedirs(complaints_dir, exist_ok=True)
        
        # Get or create a default user for the imported complaints
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Created default admin user'))
        
        # Read the HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Find all complaint cards
        complaint_cards = soup.select('div.bg-white.rounded-lg.shadow-sm.border')
        
        # Dictionary to map image filenames to their original paths
        image_mapping = {
            'gutter.jpeg': 'images/gutter.jpeg',
            'bin.jpeg': 'images/bin.jpeg',
            'light.jpeg': 'images/light.jpeg',
        }
        
        # Create complaints
        for i, card in enumerate(complaint_cards):
            try:
                # Extract data from the HTML
                username = card.select_one('h3.font-semibold').text.strip()
                time_ago = card.select_one('p.text-xs.text-gray-500').text.strip()
                description = card.select_one('p.text-gray-800').text.strip()
                location = card.select_one('p.text-black-100').text.replace('Location :', '').strip()
                
                # Extract image filename
                img_tag = card.select_one('img.w-full.h-auto.rounded')
                image_filename = os.path.basename(img_tag['src']) if img_tag and 'src' in img_tag.attrs else ''
                
                # Get status from the status span
                status_span = card.select_one('span.text-xs')
                status_text = status_span.text.lower() if status_span else 'reported'
                
                # Map status text to our status choices
                status_mapping = {
                    'reported': 'reported',
                    'in progress': 'in_progress',
                    'resolved': 'resolved'
                }
                status = 'reported'
                for key, value in status_mapping.items():
                    if key in status_text.lower():
                        status = value
                        break
                
                # Get likes count
                likes_span = card.select_one('span.like-count')
                likes = int(likes_span.text.strip()) if likes_span and likes_span.text.strip().isdigit() else 0
                
                # Create a title from the first few words of the description
                title = ' '.join(description.split()[:5]) + '...'
                
                # Create a timestamp based on the time ago text
                created_at = datetime.now() - timedelta(
                    hours=2 if 'hour' in time_ago else 
                           int(time_ago.split()[0]) if 'day' not in time_ago else 
                           int(time_ago.split()[0]) * 24
                )
                
                # Create the complaint
                complaint = Complaint.objects.create(
                    user=user,
                    title=title,
                    description=description,
                    location=location,
                    status=status,
                    likes=likes,
                    created_at=created_at
                )
                
                # Copy the image file if it exists
                if image_filename and image_filename in image_mapping:
                    src_path = os.path.join(settings.BASE_DIR, image_mapping[image_filename])
                    if os.path.exists(src_path):
                        dst_filename = f'complaint_{complaint.id}_{image_filename}'
                        dst_path = os.path.join(complaints_dir, dst_filename)
                        shutil.copy2(src_path, dst_path)
                        complaint.image = f'complaints/{dst_filename}'
                        complaint.save()
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported complaint: {title}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing complaint: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('Finished importing complaints'))
