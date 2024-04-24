from rest_framework.renderers import BaseRenderer
import json


class GradientColorRenderer(BaseRenderer):
    media_type = "text/html"
    charset = "utf-8"
    format = "html"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        style = """
            <style>
                body{
                    background-color:black
                }
                pre {
                    font-style: italic;
                    color:white;
                
                }
            </style>
        """
        pre = "<pre>{}</pre>".format(json.dumps(data, indent=4))

        script = """
          <script>
            const preTag = document.querySelector('pre');
            const colors = ['green', 'blue', 'red'];
            let index = 0;

            setInterval(() => {
                index = (index + 1) % colors.length; 
                preTag.style.color = colors[index];
            }, 3000); 

            preTag.style.transition = 'color 1s ease';
        </script>
        """

        return (style + pre + script).encode(self.charset)
