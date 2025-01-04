from app import app, FAQ

with app.app_context():
    faqs = FAQ.query.all()
    for faq in faqs:
      print(f"Question: {faq.question}, Answer: {faq.answer}, Language: {faq.language}")
