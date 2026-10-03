from django.shortcuts import render


def index(request):
	products = [
		{
			'name': 'A5 Notebook',
			'category': 'Paper goods',
			'description': 'A fresh page for lecture notes, plans, and new ideas.',
			'image': 'products/notebook.jpg',
			'image_alt': 'An open notebook ready for writing',
		},
		{
			'name': 'Everyday Backpack',
			'category': 'On the move',
			'description': 'Keep your daily study essentials together.',
			'image': 'products/backpack.jpg',
			'image_alt': 'An everyday backpack',
		},
		{
			'name': 'Desk Lamp',
			'category': 'Study space',
			'description': 'A little light for your next chapter.',
			'image': 'products/lamp.jpg',
			'image_alt': 'A lamp for a study desk',
		},
	]
	return render(request, 'products/index.html', {'products': products})


def about(request):
	return render(request, 'about.html')
