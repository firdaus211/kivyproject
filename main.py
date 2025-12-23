import kivy
# Trigger rebuild
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import numpy as np
import math
import re

# Define a custom SpinnerOption with desired colors
class CustomSpinnerOption(SpinnerOption):
    background_color = (0.9, 0.9, 0.9, 1)
    color = (0.1, 0.1, 0.1, 1)

class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.functions = []
        self.x_min = -10
        self.x_max = 10
        self.y_min = -5
        self.y_max = 5
        self.grid_size = 1
        self.bind(pos=self.update_graph, size=self.update_graph)
        Clock.schedule_once(self.update_graph)
    
    def add_function(self, expression, color, params=None):
        if params is None:
            params = {}
        self.functions.append({'expression': expression, 'color': color, 'params': params})
        self.update_graph()
    
    def remove_function(self, index):
        if 0 <= index < len(self.functions):
            del self.functions[index]
            self.update_graph()
    
    def clear_functions(self):
        self.functions = []
        self.update_graph()
    
    def set_range(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.update_graph()
    
    def update_graph(self, *args):
        self.canvas.clear()
        
        # Draw white background
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
        
        # Draw grid
        self.draw_grid()
        
        # Draw axes
        self.draw_axes()
        
        # Draw axis labels and numbers
        self.draw_axis_labels()
        
        # Draw functions
        for func in self.functions:
            self.draw_function(func['expression'], func['color'], func.get('params', {}))
    
    def draw_grid(self):
        with self.canvas:
            Color(0.85, 0.85, 0.85, 1)  # Light gray grid
            
            # Vertical lines
            x_range = self.x_max - self.x_min
            x_step = self.grid_size
            x_start = int(self.x_min / x_step) * x_step
            
            for x in np.arange(x_start, self.x_max + x_step, x_step):
                x_pos = self.pos[0] + (x - self.x_min) / x_range * self.size[0]
                Line(points=[x_pos, self.pos[1], x_pos, self.pos[1] + self.size[1]], width=1)
            
            # Horizontal lines
            y_range = self.y_max - self.y_min
            y_step = self.grid_size
            y_start = int(self.y_min / y_step) * y_step
            
            for y in np.arange(y_start, self.y_max + y_step, y_step):
                y_pos = self.pos[1] + (y - self.y_min) / y_range * self.size[1]
                Line(points=[self.pos[0], y_pos, self.pos[0] + self.size[0], y_pos], width=1)
    
    def draw_axes(self):
        with self.canvas:
            Color(0.3, 0.3, 0.3, 1)  # Dark gray axes
            
            # X-axis
            if self.y_min <= 0 <= self.y_max:
                y_pos = self.pos[1] + (0 - self.y_min) / (self.y_max - self.y_min) * self.size[1]
                Line(points=[self.pos[0], y_pos, self.pos[0] + self.size[0], y_pos], width=2)
            
            # Y-axis
            if self.x_min <= 0 <= self.x_max:
                x_pos = self.pos[0] + (0 - self.x_min) / (self.x_max - self.x_min) * self.size[0]
                Line(points=[x_pos, self.pos[1], x_pos, self.pos[1] + self.size[1]], width=2)
    
    def draw_axis_labels(self):
        # Draw axis labels and numbers
        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)  # Dark text color
            
            # X-axis labels
            x_range = self.x_max - self.x_min
            x_step = self.grid_size
            x_start = int(self.x_min / x_step) * x_step
            
            for x in np.arange(x_start, self.x_max + x_step, x_step):
                if abs(x) > 0.01:  # Skip 0 to avoid overlap with origin
                    x_pos = self.pos[0] + (x - self.x_min) / x_range * self.size[0]
                    
                    # Find y position for x-axis
                    if self.y_min <= 0 <= self.y_max:
                        y_pos = self.pos[1] + (0 - self.y_min) / (self.y_max - self.y_min) * self.size[1]
                    else:
                        y_pos = self.pos[1] + 10  # Place at bottom if x-axis not visible
                    
                    # Draw tick mark
                    tick_size = 5
                    Line(points=[x_pos, y_pos - tick_size, x_pos, y_pos + tick_size], width=1)
                    
                    # Draw number
                    label_text = str(int(x)) if x == int(x) else f"{x:.1f}"
                    label = Label(text=label_text, font_size=dp(10), color=(0.2, 0.2, 0.2, 1))
                    label.texture_update()
                    label_size = label.texture_size
                    label_pos = (x_pos - label_size[0]/2, y_pos - tick_size - label_size[1] - 2)
                    
                    with self.canvas:
                        Color(1, 1, 1, 1)
                        Rectangle(pos=label_pos, size=label_size)
                        Color(0.2, 0.2, 0.2, 1)
                        Rectangle(texture=label.texture, pos=label_pos, size=label_size)
            
            # Y-axis labels
            y_range = self.y_max - self.y_min
            y_step = self.grid_size
            y_start = int(self.y_min / y_step) * y_step
            
            for y in np.arange(y_start, self.y_max + y_step, y_step):
                if abs(y) > 0.01:  # Skip 0 to avoid overlap with origin
                    y_pos = self.pos[1] + (y - self.y_min) / y_range * self.size[1]
                    
                    # Find x position for y-axis
                    if self.x_min <= 0 <= self.x_max:
                        x_pos = self.pos[0] + (0 - self.x_min) / (self.x_max - self.x_min) * self.size[0]
                    else:
                        x_pos = self.pos[0] + 10  # Place at left if y-axis not visible
                    
                    # Draw tick mark
                    tick_size = 5
                    Line(points=[x_pos - tick_size, y_pos, x_pos + tick_size, y_pos], width=1)
                    
                    # Draw number
                    label_text = str(int(y)) if y == int(y) else f"{y:.1f}"
                    label = Label(text=label_text, font_size=dp(10), color=(0.2, 0.2, 0.2, 1))
                    label.texture_update()
                    label_size = label.texture_size
                    label_pos = (x_pos - tick_size - label_size[0] - 2, y_pos - label_size[1]/2)
                    
                    with self.canvas:
                        Color(1, 1, 1, 1)
                        Rectangle(pos=label_pos, size=label_size)
                        Color(0.2, 0.2, 0.2, 1)
                        Rectangle(texture=label.texture, pos=label_pos, size=label_size)
            
            # Draw axis labels (X and Y)
            # X label
            x_label = Label(text='X', font_size=dp(12), bold=True, color=(0.2, 0.2, 0.2, 1))
            x_label.texture_update()
            x_label_size = x_label.texture_size
            x_label_pos = (self.pos[0] + self.size[0] - x_label_size[0] - 10, 
                           self.pos[1] + 10)
            
            with self.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=x_label_pos, size=x_label_size)
                Color(0.2, 0.2, 0.2, 1)
                Rectangle(texture=x_label.texture, pos=x_label_pos, size=x_label_size)
            
            # Y label
            y_label = Label(text='Y', font_size=dp(12), bold=True, color=(0.2, 0.2, 0.2, 1))
            y_label.texture_update()
            y_label_size = y_label.texture_size
            y_label_pos = (self.pos[0] + 10, 
                           self.pos[1] + self.size[1] - y_label_size[1] - 10)
            
            with self.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=y_label_pos, size=y_label_size)
                Color(0.2, 0.2, 0.2, 1)
                Rectangle(texture=y_label.texture, pos=y_label_pos, size=y_label_size)
    
    def draw_function(self, expression, color, params):
        try:
            # Parse the expression
            safe_dict = {
                'x': 0,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'exp': math.exp,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'abs': abs,
                'ceil': math.ceil,
                'floor': math.floor,
                'round': round,
                'pi': math.pi,
                'e': math.e,
                'factorial': math.factorial if hasattr(math, 'factorial') else lambda n: 1 if n <= 1 else n * math.factorial(n-1),
                'a': params.get('a', 1),
                'b': params.get('b', 1),
                'c': params.get('c', 1),
            }
            
            # Create points for the function
            points = []
            x_values = np.linspace(self.x_min, self.x_max, 1000)
            
            for x_val in x_values:
                safe_dict['x'] = x_val
                try:
                    y_val = eval(expression, {"__builtins__": None}, safe_dict)
                    if not math.isnan(y_val) and not math.isinf(y_val):
                        x_pos = self.pos[0] + (x_val - self.x_min) / (self.x_max - self.x_min) * self.size[0]
                        y_pos = self.pos[1] + (y_val - self.y_min) / (self.y_max - self.y_min) * self.size[1]
                        points.extend([x_pos, y_pos])
                except:
                    pass
            
            # Draw the function with increased width for better visibility
            if len(points) >= 4:
                with self.canvas:
                    Color(*color)
                    Line(points=points, width=3)  # Increased line width
        except Exception as e:
            print(f"Error drawing function: {e}")

class FunctionInput(BoxLayout):
    expression = StringProperty("")
    color = ListProperty([1, 0, 0, 1])
    index = NumericProperty(-1)
    graph = ObjectProperty(None)
    is_valid = BooleanProperty(True)
    app = ObjectProperty(None)  # Add reference to app
    
    def __init__(self, index, graph, app, **kwargs):
        super(FunctionInput, self).__init__(**kwargs)
        self.index = index
        self.graph = graph
        self.app = app  # Store reference to app
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(5)
        self.spacing = dp(2)
        
        # Color picker - using vibrant colors for better contrast
        colors = [
            [0.9, 0.2, 0.2, 1],    # Bright Red
            [0.1, 0.7, 0.1, 1],    # Bright Green
            [0.1, 0.3, 0.9, 1],    # Bright Blue
            [0.8, 0.1, 0.8, 1],    # Bright Magenta
            [0.9, 0.7, 0.1, 1],    # Bright Yellow
            [0.1, 0.7, 0.7, 1],    # Bright Cyan
            [1.0, 0.5, 0.0, 1],    # Orange
            [0.6, 0.1, 0.9, 1],    # Purple
        ]
        self.color = colors[index % len(colors)]
        
        # Top row with color indicator and function input
        top_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        
        # Color indicator
        self.color_indicator = Widget(size_hint=(None, 1), width=dp(20))
        with self.color_indicator.canvas:
            Color(*self.color)
            Rectangle(pos=self.color_indicator.pos, size=self.color_indicator.size)
        
        # Function input
        self.input = TextInput(
            text=f"f{index+1}(x) = ",
            size_hint=(0.7, 1),
            multiline=False,
            font_size=dp(14),
            background_color=(0.95, 0.95, 0.95, 1),  # Light background
            foreground_color=(0.1, 0.1, 0.1, 1),     # Dark text
            cursor_color=(0.1, 0.1, 0.1, 1)
        )
        self.input.bind(text=self.on_text_change)
        
        # Template button
        self.template_btn = Button(
            text='Templates',
            size_hint=(None, 1),
            width=dp(80),
            font_size=dp(12),
            background_color=(0.3, 0.6, 0.9, 1),      # Blue button
            color=(1, 1, 1, 1)                      # White text
        )
        self.template_btn.bind(on_press=self.show_templates)
        
        # Delete button
        self.delete_btn = Button(
            text="×",
            size_hint=(None, 1),
            width=dp(40),
            font_size=dp(20),
            background_color=(0.9, 0.3, 0.3, 1),      # Red button
            color=(1, 1, 1, 1)                       # White text
        )
        self.delete_btn.bind(on_press=self.delete_function)
        
        top_row.add_widget(self.color_indicator)
        top_row.add_widget(self.input)
        top_row.add_widget(self.template_btn)
        top_row.add_widget(self.delete_btn)
        
        # Error message label
        self.error_label = Label(
            text='',
            size_hint_y=None,
            height=dp(20),
            font_size=dp(10),
            color=(0.8, 0.2, 0.2, 1),  # Red error text
            halign='left'
        )
        
        # Add widgets to layout
        self.add_widget(top_row)
        self.add_widget(self.error_label)
        
        # Update color indicator when position changes
        self.bind(pos=self.update_color_indicator)
    
    def update_color_indicator(self, *args):
        with self.color_indicator.canvas:
            self.color_indicator.canvas.clear()
            Color(*self.color)
            Rectangle(pos=self.color_indicator.pos, size=self.color_indicator.size)
    
    def on_text_change(self, instance, value):
        # Extract the expression part after "="
        if "=" in value:
            expression = value.split("=", 1)[1].strip()
            self.expression = expression
            
            # Validate expression
            is_valid, error_msg = self.validate_expression(expression)
            self.is_valid = is_valid
            
            if is_valid:
                self.error_label.text = ''
                self.input.background_color = (0.95, 0.95, 0.95, 1)  # Normal light background
                # Update the graph
                if self.graph:
                    self.graph.remove_function(self.index)
                    if expression:
                        # Use app reference to get parameter values
                        params = {
                            'a': self.app.param_a.value if hasattr(self.app, 'param_a') else 1,
                            'b': self.app.param_b.value if hasattr(self.app, 'param_b') else 1,
                            'c': self.app.param_c.value if hasattr(self.app, 'param_c') else 1
                        }
                        self.graph.add_function(expression, self.color, params)
            else:
                self.error_label.text = error_msg
                self.input.background_color = (1, 0.9, 0.9, 1)  # Light red background for error
    
    def validate_expression(self, expression):
        if not expression:
            return True, ""
        
        try:
            # Test with a sample x value
            safe_dict = {
                'x': 1,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'exp': math.exp,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'abs': abs,
                'ceil': math.ceil,
                'floor': math.floor,
                'round': round,
                'pi': math.pi,
                'e': math.e,
                'factorial': math.factorial if hasattr(math, 'factorial') else lambda n: 1 if n <= 1 else n * math.factorial(n-1),
                'a': 1, 'b': 1, 'c': 1,
            }
            
            eval(expression, {"__builtins__": None}, safe_dict)
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except NameError as e:
            return False, f"Unknown function or variable: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def show_templates(self, instance):
        # Create template popup
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Add white background
        with popup_content.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=popup_content.pos, size=popup_content.size)
        
        popup_content.add_widget(Label(text='Function Templates', font_size=dp(18), bold=True, color=(0.1, 0.1, 0.1, 1)))
        
        # Template buttons
        templates = [
            ('Linear', 'a*x + b'),
            ('Quadratic', 'a*x**2 + b*x + c'),
            ('Cubic', 'a*x**3 + b*x**2 + c*x + 1'),
            ('Sine', 'a*sin(b*x + c)'),
            ('Cosine', 'a*cos(b*x + c)'),
            ('Tangent', 'a*tan(b*x + c)'),
            ('Exponential', 'a*exp(b*x)'),
            ('Logarithmic', 'a*log(b*x + c)'),
            ('Square Root', 'a*sqrt(b*x + c)'),
            ('Absolute', 'a*abs(b*x + c)'),
            ('Reciprocal', 'a/(b*x + c)'),
            ('Power', 'a*x**b'),
            ('Sine Squared', 'a*sin(b*x)**2'),
            ('Damped Sine', 'a*exp(-b*x)*sin(c*x)'),
            ('Gaussian', 'a*exp(-(x-b)**2/c)'),
        ]
        
        template_grid = GridLayout(cols=2, spacing=dp(5))
        
        for name, formula in templates:
            btn = Button(
                text=f"{name}\n{formula}",
                halign='center',
                font_size=dp(12),
                background_color=(0.3, 0.6, 0.9, 1),  # Blue buttons
                color=(1, 1, 1, 1)                   # White text
            )
            btn.bind(on_press=lambda btn, f=formula: self.apply_template(f))
            template_grid.add_widget(btn)
        
        popup_content.add_widget(template_grid)
        
        # Close button
        close_btn = Button(text='Close', size_hint_y=None, height=dp(40), 
                          background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1))
        close_btn.bind(on_press=lambda btn: popup.dismiss())
        popup_content.add_widget(close_btn)
        
        # Create popup
        popup = Popup(title='Select Template', content=popup_content, size_hint=(0.8, 0.8))
        popup.open()
    
    def apply_template(self, formula):
        self.input.text = f"f{self.index+1}(x) = {formula}"
    
    def delete_function(self, instance):
        if self.graph:
            self.graph.remove_function(self.index)
            self.parent.remove_widget(self)

# Enhanced calculator buttons with distinct colors
class NumberButton(Button):
    def __init__(self, text, size_hint, **kwargs):
        super(NumberButton, self).__init__(**kwargs)
        self.text = text
        self.size_hint = size_hint
        self.font_size = dp(18)
        self.background_color = (0.9, 0.9, 0.9, 1)  # Light gray
        self.color = (0.1, 0.1, 0.1, 1)          # Dark text

class OperatorButton(Button):
    def __init__(self, text, size_hint, **kwargs):
        super(OperatorButton, self).__init__(**kwargs)
        self.text = text
        self.size_hint = size_hint
        self.font_size = dp(18)
        self.background_color = (0.7, 0.7, 0.8, 1)  # Light blue-gray
        self.color = (0.1, 0.1, 0.1, 1)          # Dark text

class FunctionButton(Button):
    def __init__(self, text, size_hint, **kwargs):
        super(FunctionButton, self).__init__(**kwargs)
        self.text = text
        self.size_hint = size_hint
        self.font_size = dp(16)
        self.background_color = (0.4, 0.7, 0.4, 1)  # Green
        self.color = (1, 1, 1, 1)                  # White text

class SpecialButton(Button):
    def __init__(self, text, size_hint, **kwargs):
        super(SpecialButton, self).__init__(**kwargs)
        self.text = text
        self.size_hint = size_hint
        self.font_size = dp(16)
        self.background_color = (0.8, 0.5, 0.2, 1)  # Orange
        self.color = (1, 1, 1, 1)                  # White text

class ClearButton(Button):
    def __init__(self, text, size_hint, **kwargs):
        super(ClearButton, self).__init__(**kwargs)
        self.text = text
        self.size_hint = size_hint
        self.font_size = dp(16)
        self.background_color = (0.8, 0.2, 0.2, 1)  # Red
        self.color = (1, 1, 1, 1)                  # White text

class GraphingCalculatorApp(App):
    def __init__(self, **kwargs):
        super(GraphingCalculatorApp, self).__init__(**kwargs)
        self.function_history = []
    
    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Add background to main layout
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(10))
        with header.canvas.before:
            Color(0.85, 0.85, 0.85, 1)
            Rectangle(pos=header.pos, size=header.size)
        header.add_widget(Label(text='Graphing Calculator', font_size=dp(20), bold=True, color=(0.1, 0.1, 0.1, 1)))
        settings_btn = Button(text='Settings', size_hint=(None, 1), width=dp(100),
                             background_color=(0.5, 0.5, 0.7, 1), color=(1, 1, 1, 1))
        settings_btn.bind(on_press=self.show_settings)
        history_btn = Button(text='History', size_hint=(None, 1), width=dp(100),
                           background_color=(0.5, 0.5, 0.7, 1), color=(1, 1, 1, 1))
        history_btn.bind(on_press=self.show_history)
        header.add_widget(settings_btn)
        header.add_widget(history_btn)
        main_layout.add_widget(header)
        
        # Content area
        content = BoxLayout()
        
        # Left panel for function inputs
        left_panel = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(350))
        with left_panel.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            Rectangle(pos=left_panel.pos, size=left_panel.size)
        left_panel.padding = dp(10)
        left_panel.spacing = dp(5)
        
        # Function inputs title
        left_panel.add_widget(Label(text='Functions', font_size=dp(16), bold=True, 
                                   size_hint_y=None, height=dp(30), color=(0.1, 0.1, 0.1, 1)))
        
        # Scrollable function inputs
        func_scroll = ScrollView(size_hint=(1, 0.4))
        func_inputs_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        func_inputs_layout.bind(minimum_height=func_inputs_layout.setter('height'))
        func_scroll.add_widget(func_inputs_layout)
        left_panel.add_widget(func_scroll)
        
        # Add function button
        add_func_btn = Button(text='+ Add Function', size_hint_y=None, height=dp(40),
                             background_color=(0.3, 0.7, 0.3, 1), color=(1, 1, 1, 1))
        add_func_btn.bind(on_press=self.add_function)
        left_panel.add_widget(add_func_btn)
        
        # Parameter controls
        left_panel.add_widget(Label(text='Parameters', font_size=dp(16), bold=True, 
                                   size_hint_y=None, height=dp(30), color=(0.1, 0.1, 0.1, 1)))
        
        params_layout = GridLayout(cols=2, size_hint_y=None, height=dp(120), spacing=dp(5))
        
        # Parameter a
        params_layout.add_widget(Label(text='a:', color=(0.1, 0.1, 0.1, 1)))
        self.param_a = Slider(min=0, max=5, value=1, step=0.1)
        self.param_a.bind(value=self.update_parameters)
        params_layout.add_widget(self.param_a)
        
        # Parameter b
        params_layout.add_widget(Label(text='b:', color=(0.1, 0.1, 0.1, 1)))
        self.param_b = Slider(min=0, max=5, value=1, step=0.1)
        self.param_b.bind(value=self.update_parameters)
        params_layout.add_widget(self.param_b)
        
        # Parameter c
        params_layout.add_widget(Label(text='c:', color=(0.1, 0.1, 0.1, 1)))
        self.param_c = Slider(min=0, max=5, value=1, step=0.1)
        self.param_c.bind(value=self.update_parameters)
        params_layout.add_widget(self.param_c)
        
        left_panel.add_widget(params_layout)
        
        # MASUKKAN PERSAMAAN GRAFIK SECTION
        left_panel.add_widget(Label(text='Masukkan Persamaan Grafik', font_size=dp(16), bold=True, 
                                   size_hint_y=None, height=dp(30), color=(0.1, 0.1, 0.1, 1)))
        
        # Quick equation input
        eq_input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140), spacing=dp(5))
        
        # Equation type selector
        eq_type_layout = BoxLayout(size_hint_y=None, height=dp(30))
        eq_type_layout.add_widget(Label(text='Tipe:', size_hint=(None, 1), width=dp(50), color=(0.1, 0.1, 0.1, 1)))
        self.eq_type_spinner = Spinner(
            text='Linear',
            values=['Linear', 'Kuadrat', 'Kubik', 'Sinus', 'Cosinus', 'Eksponensial', 'Logaritma', 'Custom'],
            size_hint=(1, 1),
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            option_cls=CustomSpinnerOption  # Use our custom option class
        )
        self.eq_type_spinner.bind(text=self.on_eq_type_change)
        eq_type_layout.add_widget(self.eq_type_spinner)
        eq_input_layout.add_widget(eq_type_layout)
        
        # Quick equation input
        quick_eq_layout = BoxLayout(size_hint_y=None, height=dp(40))
        quick_eq_layout.add_widget(Label(text='y =', size_hint=(None, 1), width=dp(30), color=(0.1, 0.1, 0.1, 1)))
        self.quick_eq_input = TextInput(
            text='x',
            multiline=False,
            font_size=dp(14),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            cursor_color=(0.1, 0.1, 0.1, 1)
        )
        quick_eq_layout.add_widget(self.quick_eq_input)
        eq_input_layout.add_widget(quick_eq_layout)
        
        # Add to graph button
        add_eq_btn = Button(
            text='Tambah ke Grafik',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        add_eq_btn.bind(on_press=self.add_quick_equation)
        eq_input_layout.add_widget(add_eq_btn)
        
        left_panel.add_widget(eq_input_layout)
        
        # View range controls (moved down)
        left_panel.add_widget(Label(text='Rentang Tampilan', font_size=dp(16), bold=True, 
                                   size_hint_y=None, height=dp(30), color=(0.1, 0.1, 0.1, 1)))
        
        view_layout = GridLayout(cols=2, size_hint_y=None, height=dp(120), spacing=dp(5))
        
        # X min
        view_layout.add_widget(Label(text='X Min:', color=(0.1, 0.1, 0.1, 1)))
        self.x_min_input = TextInput(text='-10', size_hint=(1, None), height=dp(30), multiline=False,
                                     background_color=(0.95, 0.95, 0.95, 1),
                                     foreground_color=(0.1, 0.1, 0.1, 1),
                                     cursor_color=(0.1, 0.1, 0.1, 1))
        view_layout.add_widget(self.x_min_input)
        
        # X max
        view_layout.add_widget(Label(text='X Max:', color=(0.1, 0.1, 0.1, 1)))
        self.x_max_input = TextInput(text='10', size_hint=(1, None), height=dp(30), multiline=False,
                                     background_color=(0.95, 0.95, 0.95, 1),
                                     foreground_color=(0.1, 0.1, 0.1, 1),
                                     cursor_color=(0.1, 0.1, 0.1, 1))
        view_layout.add_widget(self.x_max_input)
        
        # Y min
        view_layout.add_widget(Label(text='Y Min:', color=(0.1, 0.1, 0.1, 1)))
        self.y_min_input = TextInput(text='-5', size_hint=(1, None), height=dp(30), multiline=False,
                                     background_color=(0.95, 0.95, 0.95, 1),
                                     foreground_color=(0.1, 0.1, 0.1, 1),
                                     cursor_color=(0.1, 0.1, 0.1, 1))
        view_layout.add_widget(self.y_min_input)
        
        # Y max
        view_layout.add_widget(Label(text='Y Max:', color=(0.1, 0.1, 0.1, 1)))
        self.y_max_input = TextInput(text='5', size_hint=(1, None), height=dp(30), multiline=False,
                                     background_color=(0.95, 0.95, 0.95, 1),
                                     foreground_color=(0.1, 0.1, 0.1, 1),
                                     cursor_color=(0.1, 0.1, 0.1, 1))
        view_layout.add_widget(self.y_max_input)
        
        left_panel.add_widget(view_layout)
        
        # Apply view button
        apply_view_btn = Button(text='Terapkan Tampilan', size_hint_y=None, height=dp(40),
                               background_color=(0.4, 0.4, 0.8, 1), color=(1, 1, 1, 1))
        apply_view_btn.bind(on_press=self.apply_view)
        left_panel.add_widget(apply_view_btn)
        
        content.add_widget(left_panel)
        
        # Graph widget
        self.graph = GraphWidget(size_hint=(1, 1))
        content.add_widget(self.graph)
        
        main_layout.add_widget(content)
        
        # Calculator panel
        calc_panel = BoxLayout(size_hint_y=None, height=dp(200), padding=dp(5), spacing=dp(2))
        with calc_panel.canvas.before:
            Color(0.85, 0.85, 0.85, 1)
            Rectangle(pos=calc_panel.pos, size=calc_panel.size)
        
        # Create calculator buttons
        calc_buttons = GridLayout(cols=10, rows=4, spacing=dp(2))
        
        # First row
        calc_buttons.add_widget(NumberButton('7', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('8', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('9', (0.1, 0.33)))
        calc_buttons.add_widget(OperatorButton('/', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('sin', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('cos', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('tan', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('log', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('ln', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('π', (0.1, 0.33)))
        
        # Second row
        calc_buttons.add_widget(NumberButton('4', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('5', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('6', (0.1, 0.33)))
        calc_buttons.add_widget(OperatorButton('*', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('x²', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('x³', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('√', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('|x|', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('e', (0.1, 0.33)))
        calc_buttons.add_widget(OperatorButton('^', (0.1, 0.33)))
        
        # Third row
        calc_buttons.add_widget(NumberButton('1', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('2', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('3', (0.1, 0.33)))
        calc_buttons.add_widget(OperatorButton('-', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('(', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton(')', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('a', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('b', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('c', (0.1, 0.33)))
        calc_buttons.add_widget(ClearButton('Clear', (0.1, 0.33)))
        
        # Fourth row
        calc_buttons.add_widget(NumberButton('0', (0.1, 0.33)))
        calc_buttons.add_widget(NumberButton('.', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('=', (0.1, 0.33)))
        calc_buttons.add_widget(OperatorButton('+', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('x', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('1/x', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('e^x', (0.1, 0.33)))
        calc_buttons.add_widget(FunctionButton('x!', (0.1, 0.33)))
        calc_buttons.add_widget(SpecialButton('%', (0.1, 0.33)))
        calc_buttons.add_widget(ClearButton('Del', (0.1, 0.33)))
        
        calc_panel.add_widget(calc_buttons)
        
        # Bind calculator buttons
        for child in calc_buttons.children:
            if isinstance(child, (NumberButton, OperatorButton, FunctionButton, SpecialButton, ClearButton)):
                child.bind(on_press=self.on_calculator_button)
        
        main_layout.add_widget(calc_panel)
        
        # Store references
        self.func_inputs_layout = func_inputs_layout
        self.function_count = 0
        
        # Add initial function
        self.add_function(None)
        
        return main_layout
    
    def add_function(self, instance):
        func_input = FunctionInput(self.function_count, self.graph, self)  # Pass self (app) as third parameter
        self.func_inputs_layout.add_widget(func_input)
        self.function_count += 1
    
    def on_eq_type_change(self, spinner, text):
        # Pre-fill equation based on selected type
        equations = {
            'Linear': 'a*x + b',
            'Kuadrat': 'a*x**2 + b*x + c',
            'Kubik': 'a*x**3 + b*x**2 + c*x',
            'Sinus': 'a*sin(b*x + c)',
            'Cosinus': 'a*cos(b*x + c)',
            'Eksponensial': 'a*exp(b*x)',
            'Logaritma': 'a*log(b*x + c)',
            'Custom': ''
        }
        self.quick_eq_input.text = equations.get(text, '')
    
    def add_quick_equation(self, instance):
        equation = self.quick_eq_input.text.strip()
        if equation:
            # Add to history
            self.function_history.append(equation)
            
            # Create a new function input with this equation
            func_input = FunctionInput(self.function_count, self.graph, self)  # Pass self (app) as third parameter
            func_input.input.text = f"f{self.function_count+1}(x) = {equation}"
            self.func_inputs_layout.add_widget(func_input)
            self.function_count += 1
            
            # Clear the quick input
            self.quick_eq_input.text = ''
    
    def on_calculator_button(self, instance):
        # Get the currently focused text input
        focused_widget = Window.focus
        if isinstance(focused_widget, TextInput):
            if instance.text == 'Clear':
                focused_widget.text = focused_widget.text.split('=')[0] + '= '
            elif instance.text == 'Del':
                if len(focused_widget.text) > 0:
                    focused_widget.text = focused_widget.text[:-1]
            elif instance.text == 'x²':
                focused_widget.text += '**2'
            elif instance.text == 'x³':
                focused_widget.text += '**3'
            elif instance.text == '√':
                focused_widget.text += 'sqrt('
            elif instance.text == '|x|':
                focused_widget.text += 'abs('
            elif instance.text == 'ln':
                focused_widget.text += 'log('
            elif instance.text == '1/x':
                focused_widget.text += '1/'
            elif instance.text == 'e^x':
                focused_widget.text += 'exp('
            elif instance.text == 'x!':
                focused_widget.text += 'factorial('
            elif instance.text == 'π':
                focused_widget.text += 'pi'
            elif instance.text == 'x':
                focused_widget.text += 'x'
            else:
                focused_widget.text += instance.text
    
    def update_parameters(self, instance, value):
        # Update all functions with new parameter values
        for i, func_input in enumerate(self.func_inputs_layout.children):
            if func_input.expression:
                params = {
                    'a': self.param_a.value,
                    'b': self.param_b.value,
                    'c': self.param_c.value
                }
                # Update the function in the graph
                if i < len(self.graph.functions):
                    self.graph.functions[i]['params'] = params
        self.graph.update_graph()
    
    def apply_view(self, instance):
        try:
            x_min = float(self.x_min_input.text)
            x_max = float(self.x_max_input.text)
            y_min = float(self.y_min_input.text)
            y_max = float(self.y_max_input.text)
            
            if x_min < x_max and y_min < y_max:
                self.graph.set_range(x_min, x_max, y_min, y_max)
        except ValueError:
            pass
    
    def show_settings(self, instance):
        # Create a settings popup
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Add white background
        with popup_content.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=popup_content.pos, size=popup_content.size)
        
        popup_content.add_widget(Label(text='Settings', font_size=dp(20), bold=True, color=(0.1, 0.1, 0.1, 1)))
        
        # Grid size setting
        grid_layout = GridLayout(cols=2, size_hint_y=None, height=dp(40))
        grid_layout.add_widget(Label(text='Grid Size:', color=(0.1, 0.1, 0.1, 1)))
        grid_size_input = TextInput(text='1', size_hint=(0.5, None), height=dp(30), multiline=False,
                                    background_color=(0.95, 0.95, 0.95, 1),
                                    foreground_color=(0.1, 0.1, 0.1, 1),
                                    cursor_color=(0.1, 0.1, 0.1, 1))
        grid_layout.add_widget(grid_size_input)
        popup_content.add_widget(grid_layout)
        
        # Line width setting
        line_layout = GridLayout(cols=2, size_hint_y=None, height=dp(40))
        line_layout.add_widget(Label(text='Line Width:', color=(0.1, 0.1, 0.1, 1)))
        line_width_input = TextInput(text='3', size_hint=(0.5, None), height=dp(30), multiline=False,
                                     background_color=(0.95, 0.95, 0.95, 1),
                                     foreground_color=(0.1, 0.1, 0.1, 1),
                                     cursor_color=(0.1, 0.1, 0.1, 1))
        line_layout.add_widget(line_width_input)
        popup_content.add_widget(line_layout)
        
        # Buttons
        buttons_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        save_btn = Button(text='Save', background_color=(0.3, 0.7, 0.3, 1), color=(1, 1, 1, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.8, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        
        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(cancel_btn)
        
        popup_content.add_widget(buttons_layout)
        
        # Create popup
        popup = Popup(title='Settings', content=popup_content, size_hint=(0.8, 0.8))
        
        # Bind buttons
        def save_settings(instance):
            try:
                grid_size = float(grid_size_input.text)
                line_width = float(line_width_input.text)
                
                self.graph.grid_size = grid_size
                # Update line width for all functions
                self.graph.update_graph()
                
                popup.dismiss()
            except ValueError:
                pass
        
        cancel_btn.bind(on_press=popup.dismiss)
        save_btn.bind(on_press=save_settings)
        
        popup.open()
    
    def show_history(self, instance):
        # Create history popup
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Add white background
        with popup_content.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=popup_content.pos, size=popup_content.size)
        
        popup_content.add_widget(Label(text='Function History', font_size=dp(18), bold=True, color=(0.1, 0.1, 0.1, 1)))
        
        # History list
        history_scroll = ScrollView(size_hint=(1, 0.8))
        history_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        history_layout.bind(minimum_height=history_layout.setter('height'))
        
        if not self.function_history:
            history_layout.add_widget(Label(text='No history yet', size_hint_y=None, height=dp(30), color=(0.1, 0.1, 0.1, 1)))
        else:
            for i, expr in enumerate(self.function_history):
                btn = Button(
                    text=expr,
                    size_hint_y=None,
                    height=dp(40),
                    halign='left',
                    background_color=(0.3, 0.6, 0.9, 1),
                    color=(1, 1, 1, 1)
                )
                btn.bind(on_press=lambda btn, e=expr: self.apply_history(e))
                history_layout.add_widget(btn)
        
        history_scroll.add_widget(history_layout)
        popup_content.add_widget(history_scroll)
        
        # Close button
        close_btn = Button(text='Close', size_hint_y=None, height=dp(40),
                          background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1))
        close_btn.bind(on_press=lambda btn: popup.dismiss())
        popup_content.add_widget(close_btn)
        
        # Create popup
        popup = Popup(title='History', content=popup_content, size_hint=(0.8, 0.8))
        popup.open()
    
    def apply_history(self, expression):
        # Apply the selected history expression to the current focused input
        focused_widget = Window.focus
        if isinstance(focused_widget, TextInput):
            if '=' in focused_widget.text:
                focused_widget.text = focused_widget.text.split('=')[0] + f'= {expression}'
            else:
                focused_widget.text = f'f(x) = {expression}'

if __name__ == '__main__':
    Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
    GraphingCalculatorApp().run()
