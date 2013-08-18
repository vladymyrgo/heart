import time

class TotalTime(object):
    def process_request(self, request):
        self.t = time.time()
    
    def process_response(self, request, response):
        delta = """<ul class="ulResults">
        <li type="none">Response took %s seconds</li>
        """ % str(
                round(
                    time.time()-self.t,
                    2)
                )
        
        response.content = response.content.replace(
                    '<ul class="ulResults">', delta)

        return response