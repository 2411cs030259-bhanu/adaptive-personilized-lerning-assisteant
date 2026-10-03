from .base import LLMProvider
class DemoLLM(LLMProvider):
    def generate_answer(self,question,context):
        return f"Demo Tutor\n\nQuestion: {question}\n\n{('Based on your uploaded material:\n'+context[:1800]) if context else 'No uploaded context was found. Upload study material to ground the answer.'}"
    def generate_quiz(self,topic,context,count,difficulty):
        templates=[
            (f"Which concept is most directly associated with {topic}?",[topic,"Rendering","UI styling","Version control"],topic),
            (f"What should you do first when studying {topic}?",["Understand the definition and conditions","Skip examples","Memorize unrelated code","Avoid practice"],"Understand the definition and conditions"),
            (f"What is the main purpose of focused practice in {topic}?",["Strengthen retrieval and understanding","Remove feedback","Increase confusion","Avoid revision"],"Strengthen retrieval and understanding"),
            (f"Which approach best checks understanding of {topic}?",["Explain it with an example","Only reread the heading","Ignore mistakes","Skip questions"],"Explain it with an example")]
        return [{"question":q,"question_type":"mcq","options":o,"correct_answer":a,"explanation":f"This answer best matches the learning goal for {topic}.","topic":topic,"difficulty":difficulty,"source_material":"student materials"} for q,o,a in [templates[i%len(templates)] for i in range(count)]]
