from django.core.management.base import BaseCommand
from dealers.models import Dealer, CarMake, CarModel


class Command(BaseCommand):
    help = "Create clearly labeled synthetic demo dealers and car makes"

    def handle(self, *args, **kwargs):
        # Addresses for the generated dealerships are synthetic examples.
        first = [
            ("Sunflower Auto Center", "Wichita", "Kansas", "1200 East Douglas Ave", "67202"),
            ("Prairie Motors", "Topeka", "Kansas", "415 Kansas Ave", "66603"),
            ("Heartland Cars", "Overland Park", "Kansas", "7900 Metcalf Ave", "66204"),
            ("Metro Auto Gallery", "Denver", "Colorado", "2100 Market St", "80205"),
            ("Lakeside Motors", "Chicago", "Illinois", "900 Lake St", "60601"),
        ]
        locations = [
            ("Wichita", "Kansas", "67202"), ("Topeka", "Kansas", "66603"),
            ("Denver", "Colorado", "80205"), ("Chicago", "Illinois", "60601"),
            ("Austin", "Texas", "78701"), ("Dallas", "Texas", "75201"),
            ("Seattle", "Washington", "98101"), ("Phoenix", "Arizona", "85001"),
            ("Miami", "Florida", "33101"), ("Boston", "Massachusetts", "02108"),
            ("Atlanta", "Georgia", "30303"), ("New York", "New York", "10001"),
            ("San Francisco", "California", "94102"), ("Portland", "Oregon", "97201"),
            ("Los Angeles", "California", "90001"),
        ]
        for number in range(1, 46):
            city, state, zipcode = locations[(number - 1) % len(locations)]
            first.append((
                f"Demo Car Dealer {number:02d}", city, state,
                f"{100 + number} Sample Avenue", zipcode,
            ))
        for name, city, state, address, zip_code in first:
            Dealer.objects.update_or_create(
                name=name,
                defaults={
                    "city": city, "state": state, "address": address,
                    "zip_code": zip_code, "phone": "555-0100",
                    "description": f"Example dealership listing for {city}. Demo data.",
                },
            )
        makes = {
            "NISSAN": ["Pathfinder", "Qashqai", "XTRAIL"],
            "Mercedes": ["A-Class", "C-Class", "E-Class"],
            "Audi": ["A4", "A5", "A6"],
            "Kia": ["Sorrento", "Carnival", "Cerato"],
            "Toyota": ["Corolla", "Camry", "Kluger", "RAV4"],
            "Honda": ["Civic", "Accord", "CR-V"],
            "Ford": ["Focus", "Mustang", "Escape"],
            "Hyundai": ["Elantra", "Tucson"],
        }
        for name, models in makes.items():
            make, _ = CarMake.objects.get_or_create(name=name)
            for model in models:
                CarModel.objects.get_or_create(make=make, name=model)
        self.stdout.write(self.style.SUCCESS(
            f"Demo records ready: {Dealer.objects.count()} dealers"
        ))
