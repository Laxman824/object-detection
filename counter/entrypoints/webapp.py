# from io import BytesIO

# from flask import Flask, request, jsonify

# from counter import config

# def create_app():
    
#     app = Flask(__name__)
    
#     count_action = config.get_count_action()
    
#     @app.route('/object-count', methods=['POST'])
#     def object_detection():
        
#         threshold = float(request.form.get('threshold', 0.5))
#         uploaded_file = request.files['file']
#         model_name = request.form.get('model_name', "rfcn")
#         image = BytesIO()
#         uploaded_file.save(image)
#         count_response = count_action.execute(image, threshold)
#         return jsonify(count_response)
    
#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run('0.0.0.0', debug=True)
#V1 BASIC WITOUT HOMEWORK
# from io import BytesIO
# from flask import Flask, request, jsonify
# from counter import config

# def create_app():
#     app = Flask(__name__)
#     count_action = config.get_count_action()
    
#     @app.route('/object-count', methods=['POST'])
#     def object_detection():
#         threshold = float(request.form.get('threshold', 0.5))
#         uploaded_file = request.files['file']
#         model_name = request.form.get('model_name', "rfcn")
#         image = BytesIO()
#         uploaded_file.save(image)
#         count_response = count_action.execute(image, threshold)
#         return jsonify(count_response)
    
#     # Add a home route for better UX
#     @app.route('/')
#     def home():
#         return """
#         <h1>Object Detection API</h1>
#         <p>Available endpoints:</p>
#         <ul>
#             <li><code>POST /object-count</code> - Detect and count objects in images</li>
#         </ul>
#         """
    
#     return app

# # Create the app instance
# app = create_app()

# if __name__ == '__main__':
#     app.run('0.0.0.0', debug=True)

from io import BytesIO
from flask import Flask, request, jsonify
from counter import config

def create_app():
    app = Flask(__name__)
    count_action = config.get_count_action()
    
    @app.route('/object-count', methods=['POST'])
    def object_detection():
        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files['file']
        model_name = request.form.get('model_name', "rfcn")
        image = BytesIO()
        uploaded_file.save(image)
        count_response = count_action.execute(image, threshold)
        return jsonify(count_response)
    
    @app.route('/predict', methods=['POST'])
    def predict():
        """New endpoint for raw predictions"""
        try:
            # Get parameters
            threshold = float(request.form.get('threshold', 0.5))
            uploaded_file = request.files['file']
            model_name = request.form.get('model_name', "rfcn")
            
            # Process image
            image = BytesIO()
            uploaded_file.save(image)
            
            # Get detector from config
            detector = config.get_object_detector()
            
            # Get predictions
            predictions = detector.predict(image)
            
            # Filter by threshold
            from counter.domain.predictions import over_threshold
            filtered_predictions = list(over_threshold(predictions, threshold))
            
            # Convert to dictionary for JSON response
            response = {
                'predictions': [
                    {
                        'class_name': p.class_name,
                        'score': p.score,
                        'box': {
                            'xmin': p.box.xmin,
                            'ymin': p.box.ymin,
                            'xmax': p.box.xmax,
                            'ymax': p.box.ymax
                        }
                    } for p in filtered_predictions
                ]
            }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/')
    def home():
        return """
        <h1>Object Detection API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><code>POST /object-count</code> - Detect and count objects in images</li>
            <li><code>POST /predict</code> - Get raw predictions with bounding boxes</li>
        </ul>
        """
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)