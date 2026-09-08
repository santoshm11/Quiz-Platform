import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from quiz.models import MCQQuestion
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from channels.db import database_sync_to_async

class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'start_quiz':
            await self.channel_layer.group_send(
                "participants",
                {
                    'type': 'redirect_to_countdown',
                }
            )
            await self.start_quiz()
    
    @database_sync_to_async
    def get_questions(self):
        return list(MCQQuestion.objects.all())

    async def start_quiz(self):
        question_objs = await self.get_questions()
        questions = []
        for q in question_objs:
            questions.append({
                'id': q.id,
                'question_name': q.question_name,
                'option1': q.option1,
                'option2': q.option2,
                'option3': q.option3,
                'option4': q.option4,
                'correct_answer': q.correct_answer,
                'category': q.category,
                'duration': q.duration,
            })
        for index, question in enumerate(questions):
            # Wait for 5 seconds (countdown period)
            print("waiting for Countdown to finish 1-------------------->")
            await asyncio.sleep(7)

            cache.set('current_question', question)
            print(f"Sending question {question['question_name']}-------------------->")

            # Send the question to all participants
            await self.channel_layer.group_send(
                "participants",
                {
                    'type': 'send_question',
                    'question_id': question['id'],
                    'question': question['question_name'],
                    'options': [
                        question['option1'],
                        question['option2'],
                        question['option3'],
                        question['option4'],
                    ],
                    'duration': question['duration'] ,
                }
            )
            
            # Wait for 30 seconds (time allotted for answering the question)
            t = question['duration'] +2
            print(f"Waiting {t} seconds for answer...-------------------->")
            print(question['duration'])
            await asyncio.sleep(t)

            print(f"Revealing answer status {question['correct_answer']}-------------------->")

            # Optionally, send the correct answer after the question time has elapsed
            await self.channel_layer.group_send(
                "participants",
                {
                    'type': 'reveal_answer',
                }
            )
            if index == len(questions) - 1:
                print("Quiz finished! Redirecting to result page.")
                await asyncio.sleep(6)  # small pause after reveal
                await self.channel_layer.group_send(
                "participants",
                {
                    'type': 'redirect_to_result',  # NEW TYPE
                }
                )
            else:
                print("waiting for Countdown to finish 2-------------------->")

                await self.channel_layer.group_send(
                    "participants",
                    {
                        'type': 'redirect_to_countdown',
                }   
                )
                await asyncio.sleep(6)
                print("Sent countdown -------------------->")

class ParticipantConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("participants", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("participants", self.channel_name)

    async def redirect_to_countdown(self, event):
        await self.send(text_data=json.dumps({
            'type': 'redirect',
            'target_url': '/countdown/'
        }))

    async def send_question(self, event):
        current_question = cache.get('current_question')
        if current_question:
            await self.send(text_data=json.dumps({
            'type': 'question',
            'question_id': current_question['id'],
            'question': current_question['question_name'],
            'options': [
                current_question['option1'],
                current_question['option2'],
                current_question['option3'],
                current_question['option4'],
            ],
            'duration': current_question['duration']  # Dynamic duration
    }))

    async def reveal_answer(self, event):
        current_question = cache.get('current_question')
        await self.send(text_data=json.dumps({            
            'type': 'answer',
            'answer': current_question['correct_answer']
        }))
    
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'store_uucms_id':
            cache_key = f"uucms_id_{self.channel_name}"
            cache.set(cache_key, data['uucms_id'], timeout=3600) 
            print(f"Stored UUCMS_ID in cache: {cache.get(cache_key)}")
            return
    
        if data['type'] == 'answer':
            uucms_id = data['uucms_id'] 
            answer = data['answer']
            print(f"Participant with UUCMS_ID ({uucms_id}) submitted answer: {answer}")
            # Optionally, you can send a confirmation back
            await self.send(text_data=json.dumps({
                'type': 'confirmation',
                'message': f'Answer received: {answer}'
            }))
    
    async def redirect_to_result(self, event):
        await self.send(text_data=json.dumps({
            'action': 'redirect_to_result',
            'url': '/result/'
        }))
