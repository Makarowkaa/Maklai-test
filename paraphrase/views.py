from django.http import JsonResponse
from rest_framework.views import APIView
from paraphrase.paraphrase_core.paraphrase_logic import Paraphraser


class ParaphraseView(APIView):
    def get(self, request):
        tree = request.GET.get('tree')
        limit = request.GET.get('limit', 20)

        if not tree:
            return JsonResponse({'error': "The 'tree' parameter is required."}, status=400)

        try:
            limit = int(limit)
        except ValueError:
            return JsonResponse({'error': "The 'limit' parameter must be an integer."}, status=400)

        paraphraser = Paraphraser(tree, limit)
        result = paraphraser.generate_paraphrases()

        return JsonResponse(result, json_dumps_params={'indent': 2, 'ensure_ascii': False})
