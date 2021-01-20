from django.http import JsonResponse

from cride.circles.models import Circle

def list_circles(request):

  circles = Circle.objects.all()
  public = circles.filter(is_public=False)
  data = []
  for circle in public:
    data.append({
      'name': circle.name,
      'slug_name': circle.slug_name,
      'rides_taken': circle.rides_taken,
      'rides_offered': circle.rides_offered,
      'members_limit': circle.members_limit,
    })
  return JsonResponse(data, safe=False)