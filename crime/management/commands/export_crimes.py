import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from crime.models import Crime

class Command(BaseCommand):
    help = 'Export crimes data to CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default=f'crimes_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv',
            help='Specify output CSV file path'
        )
        parser.add_argument(
            '--since',
            help='Export crimes since date (YYYY-MM-DD)'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        since_date = options.get('since')

        # Get queryset
        queryset = Crime.objects.all().order_by('-created_at')
        if since_date:
            queryset = queryset.filter(created_at__gte=since_date)

        # Define CSV headers
        fieldnames = [
            'id',
            'name',
            'description',
            'count',
            'created_at',
            'updated_at'
        ]

        try:
            with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                # Write data
                total_records = queryset.count()
                self.stdout.write(f'Starting export of {total_records} records...')

                for crime in queryset:
                    writer.writerow({
                        'id': crime.id,
                        'name': crime.name,
                        'description': crime.description,
                        'count': crime.count if crime.count is not None else '',
                        'created_at': crime.created_at.isoformat(),
                        'updated_at': crime.updated_at.isoformat(),
                    })

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully exported {total_records} crimes to {output_file}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error exporting crimes: {str(e)}')
            )