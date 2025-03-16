import os
import csv
import tempfile
from django.core.management.base import BaseCommand
from main.models import DrinkType
from kaggle.api.kaggle_api_extended import KaggleApi
from django.conf import settings

class Command(BaseCommand):
    help = 'Import coffee shop data from Kaggle dataset'

    def add_arguments(self, parser):
        parser.add_argument('--dataset', type=str, help='Kaggle dataset name (username/dataset-name)')
        parser.add_argument('--filename', type=str, help='CSV filename within the dataset')

    def handle(self, *args, **options):
        # Get dataset info from arguments or environment variables
        dataset = options.get('dataset') or os.environ.get('KAGGLE_DATASET')
        filename = options.get('filename') or os.environ.get('KAGGLE_FILENAME')
        
        if not dataset or not filename:
            self.stderr.write(self.style.ERROR(
                'Please provide dataset and filename either as command arguments or environment variables'
            ))
            return
            
        self.stdout.write(self.style.SUCCESS(f'Authenticating with Kaggle API'))
        
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()
        
        # Create a temporary directory to download the dataset
        with tempfile.TemporaryDirectory() as temp_dir:
            self.stdout.write(self.style.SUCCESS(f'Downloading dataset {dataset}'))
            
            # Download the dataset
            api.dataset_download_file(
                dataset=dataset,
                file_name=filename,
                path=temp_dir
            )
            
            # Path to the downloaded file
            file_path = os.path.join(temp_dir, filename)
            
            # Clear existing data if requested
            DrinkType.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing drink data'))
            
            # Import data from CSV
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                
                for row in reader:
                    # Clean up any extra commas in the CSV
                    price_small = row['price_small'].strip(',')
                    price_medium = row['price_medium'].strip(',')
                    price_large = row['price_large'].strip(',')
                    simple_value = row['simple'].strip(',')
                    double_value = row['double'].strip(',')
                    
                    # Handle empty price values
                    price_small = float(price_small) if price_small else 0.0
                    price_medium = float(price_medium) if price_medium else 0.0
                    price_large = float(price_large) if price_large else 0.0
                    simple = float(simple_value) if simple_value else 0.0
                    double = float(double_value) if double_value else 0.0
                    
                    # Create drink type
                    DrinkType.objects.create(
                        drink_type=row['drink_type'],
                        price_small=price_small,
                        price_medium=price_medium,
                        price_large=price_large,
                        simple=simple,
                        double=double
                    )
                    count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} drink types from Kaggle'))