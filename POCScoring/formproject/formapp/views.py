from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Form, Section, Question, Employee, Response, Subsection, Question, FormAssignment
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render
import json
from . import views
from collections import namedtuple
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


def delete_form(request, form_id):
    form = Form.objects.get(id=form_id)
    form.delete()
    return redirect('admin_dashboard')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Now we need to check if the user is an admin or a normal employee.
                try:
                    employee = Employee.objects.get(user=user)
                    if user.is_superuser:  # check if the user is superuser
                        return redirect('admin_dashboard')
                    else:
                        return redirect('employee_dashboard')
                except Employee.DoesNotExist:
                    return HttpResponse("Invalid user", status=400)
            else:
                # Invalid login credentials provided.
                return render(request, 'formapp/employee_login.html', {'error': 'Invalid login credentials.'})
        else:
            # Either username or password not provided.
            return render(request, 'formapp/employee_login.html', {'error': 'Both fields are required.'})
    else:
        return render(request, 'formapp/employee_login.html')




def employee_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            return HttpResponse("Employee does not exist.")
        
        form_assignments = FormAssignment.objects.filter(employee=employee, completed=False)
        completed_form_assignments = FormAssignment.objects.filter(employee=employee, completed=True)
        
        return render(request, 'formapp/employee_dashboard.html', {
            'employee_name': user.username,
            'form_assignments': form_assignments,
            'completed_form_assignments': completed_form_assignments
        })
    else:
        return HttpResponse("You are not logged in.")

def admin_dashboard(request):
    # Get a list of all forms
    forms = Form.objects.all()

    # Get a list of all completed form assignments
    completed_form_assignments = FormAssignment.objects.filter(completed=True)

    # Constructing a list of dictionaries, each containing the details of a completed form
    completed_forms = []
    for assignment in completed_form_assignments:
        form_details = {
            'form_title': assignment.form.title,
            'employee_name': assignment.employee.user.username,
            'assignment_id': assignment.id,  # include assignment_id in form details
            # include more details as needed
        }
        completed_forms.append(form_details)

    context = {
        'forms': forms,
        'completed_forms': completed_forms,
    }
    return render(request, 'formapp/admin_dashboard.html', context)



def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(FormAssignment, pk=assignment_id)

    question_responses = []
    for question in Question.objects.filter(subsection__section__form=assignment.form):
        try:
            response = Response.objects.get(assignment=assignment, question=question)
            question_responses.append({
                'question': question,
                'response': response,
            })
        except Response.DoesNotExist:
            continue

    context = {
        "assignment": assignment,
        "question_responses": question_responses,
    }
    return render(request, 'formapp/assignment_detail.html', context)





def form_view(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    sections = Section.objects.filter(form=form)
    subsections = Subsection.objects.filter(section__in=sections)
    questions = Question.objects.filter(subsection__in=subsections)
    return render(request, 'formapp/admin_form_detail.html', {
        'form': form,
        'sections': sections,
        'subsections': subsections,
        'questions': questions,
    })

def form_submit(request, assignment_id):
    assignment = get_object_or_404(FormAssignment, id=assignment_id)
    form = assignment.form
    if request.method == 'POST':
        data = json.loads(request.body)  # Load JSON data from request body
        for section in form.section_set.all():
            for subsection in section.subsection_set.all():  # Iterate over subsections within a section
                for question in subsection.question_set.all():  # Iterate over questions within a subsection
                    score = data.get(str(question.id))
                    if score is not None and 0 <= int(score) <= 5:  # Check that score is between 0 and 5
                        Response.objects.create(
                            assignment=assignment,
                            question=question,
                            score=score
                        )
                    else:
                        return JsonResponse({
                            "error": f"Score for question id {question.id} not provided or out of range (0-5)",
                        }, status=400)
        assignment.completed = True  # Mark the assignment as completed
        assignment.save()

        if request.user.is_staff:
            return redirect(reverse('admin_dashboard'))
        else:
            return redirect(reverse('employee_dashboard'))
    else:  # This part will display the form to submit responses
        sections = form.section_set.all()
        subsections = Subsection.objects.filter(section__in=sections)
        questions = Question.objects.filter(subsection__in=subsections)
        return render(request, 'formapp/form_completion.html', {
            'assignment': assignment,
            'sections': sections,
            'subsections': subsections,  # Pass subsections to template
            'questions': questions,
        })





@csrf_exempt
def form_create(request):
    if request.method == 'POST':
        # Load JSON data from request body
        data = json.loads(request.body)

        form_title = data.get('form_title')
        sections_data = data.get('sections')  # this will be a list of dictionaries

        if form_title and sections_data:
            form = Form.objects.create(title=form_title, creator=request.user, is_draft=True)
            
            for section_data in sections_data:
                section = Section.objects.create(title=section_data['title'], form=form)
                for subsection_data in section_data['subsections']:
                    subsection = Subsection.objects.create(title=subsection_data['title'], section=section)
                    for question_data in subsection_data['questions']:
                        Question.objects.create(text=question_data['text'], subsection=subsection)
            
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Form title and sections are required."}, status=400)
    else:
        # this will be run for GET requests
        return render(request, 'formapp/form_creation.html')

def form_assignment(request, form_id=None):
    if form_id is not None:
        form = get_object_or_404(Form, id=form_id)
        if request.method == 'POST':
            employee_ids = request.POST.getlist('employees')
            employees = Employee.objects.filter(id__in=employee_ids)
            if employees:
                form.assigned_employees.add(*employees)
                return redirect('admin_dashboard')
            else:
                return HttpResponse("Invalid employee id(s) provided", status=400)
        else:
            employees = Employee.objects.all()
            return render(request, 'formapp/form_assignment.html', {'form': form, 'employees': employees})
    else:
        forms = Form.objects.all()
        return render(request, 'formapp/form_assignment.html', {'forms': forms})



def form_assignment_list(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    employees = form.assigned_employees.all()  # Fetches all employees assigned this form

    return render(request, 'formapp/form_assignment_list.html', {'form': form, 'employees': employees})

    
@csrf_exempt
def form_detail(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    sections = form.sections.all()
    employees = form.assigned_employees.all()

    if request.method == 'POST':
        data = json.loads(request.body)

        # Update form title
        form.title = data.get('form_title')
        form.save()

        # Update existing sections, subsections, and questions and create new ones
        sections_data = data.get('sections', [])
        for section_data in sections_data:
            section_id = section_data.get('id')
            if section_id:
                # Update existing section
                section = Section.objects.get(id=section_id)
                section.title = section_data['title']
                section.save()

                # Handle subsections
                subsections_data = section_data.get('subsections', [])
                for subsection_data in subsections_data:
                    subsection_id = subsection_data.get('id')
                    if subsection_id:
                        # Update existing subsection
                        subsection = Subsection.objects.get(id=subsection_id)
                        subsection.title = subsection_data['title']
                        subsection.save()

                        # Handle questions
                        questions_data = subsection_data.get('questions', [])
                        for question_data in questions_data:
                            question_id = question_data.get('id')
                            if question_id:
                                # Update existing question
                                question = Question.objects.get(id=question_id)
                                question.text = question_data['text']
                                question.save()
                            else:
                                # Create new question
                                Question.objects.create(text=question_data['text'], subsection=subsection)
                    else:
                        # Create new subsection and associated questions
                        new_subsection = Subsection.objects.create(title=subsection_data['title'], section=section)
                        questions_data = subsection_data.get('questions', [])
                        for question_data in questions_data:
                            Question.objects.create(text=question_data['text'], subsection=new_subsection)
            else:
                # Create new section and associated subsections and questions
                new_section = Section.objects.create(title=section_data['title'], form=form)
                subsections_data = section_data.get('subsections', [])
                for subsection_data in subsections_data:
                    new_subsection = Subsection.objects.create(title=subsection_data['title'], section=new_section)
                    questions_data = subsection_data.get('questions', [])
                    for question_data in questions_data:
                        Question.objects.create(text=question_data['text'], subsection=new_subsection)

        return JsonResponse({"status": "success"})

    else:
        context = {
            'form': form,
            'sections': sections,
            'employees': employees,
        }
        return render(request, 'formapp/form_detail.html', context)


@csrf_exempt
def save_draft(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body)

            form_title = form_data.get('form_title')
            if not form_title:
                return JsonResponse({'status': 'error', 'error': 'Invalid form title.'})

            form, created = Form.objects.get_or_create(title=form_title, creator=request.user)
        
            sections = form_data.get('sections')
            if not sections:
                return JsonResponse({'status': 'error', 'error': 'Invalid or missing sections data.'})

            for section_order, section_data in enumerate(sections):
                section_title = section_data.get('title')
                if not section_title:
                    return JsonResponse({'status': 'error', 'error': 'Invalid section title.'})

                section, created = Section.objects.get_or_create(title=section_title, form=form, order=section_order)
                
                subsections = section_data.get('subsections')
                if not subsections:
                    return JsonResponse({'status': 'error', 'error': 'Invalid or missing subsections data.'})

                for subsection_order, subsection_data in enumerate(subsections):
                    subsection_title = subsection_data.get('title')
                    if not subsection_title:
                        return JsonResponse({'status': 'error', 'error': 'Invalid subsection title.'})

                    subsection, created = Subsection.objects.get_or_create(title=subsection_title, section=section, order=subsection_order)

                    questions = subsection_data.get('questions')
                    if not questions:
                        return JsonResponse({'status': 'error', 'error': 'Invalid or missing questions data.'})

                    for question_order, question_data in enumerate(questions):
                        question_text = question_data.get('text')
                        if not question_text:
                            return JsonResponse({'status': 'error', 'error': 'Invalid question text.'})

                        question, created = Question.objects.get_or_create(text=question_text, subsection=subsection, order=question_order)

            return JsonResponse({'status': 'success', 'url': reverse('admin_dashboard')})

        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e), 'url': reverse('admin_dashboard')})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method.'})


def employee_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    forms = employee.form_set.all()  # Fetches all forms associated with this employee
    return render(request, 'formapp/employee_view.html', {'employee': employee, 'forms': forms})

def employee_manage(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')

        # Check if creating a new employee or updating existing
        if employee_id:
            # Updating existing employee
            employee = get_object_or_404(Employee, id=employee_id)
            if new_username:
                try:
                    employee.user.username = new_username
                    employee.user.full_clean()  # This will check the validation for username.
                except ValidationError as e:
                    # Handle the case when username is not unique
                    # You can render the same page with error message.
                    return render(request, 'formapp/admin_employee_management.html', {'error': e.messages})
            if new_password:
                employee.user.set_password(new_password)  # Hashes the password
            employee.user.save()

        else:
            # Creating new employee
            try:
                user = User.objects.create_user(username=new_username, password=new_password)
                employee = Employee.objects.create(user=user)
            except ValidationError as e:
                # Handle the case when username is not unique
                # You can render the same page with error message.
                return render(request, 'formapp/admin_employee_management.html', {'error': e.messages})

        return redirect('admin_dashboard')

    else:
        employees = Employee.objects.all()
        return render(request, 'formapp/admin_employee_management.html', {'employees': employees})
    
def form_score_view(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if request.method == 'GET':
        sections = Section.objects.filter(form=form)
        subsections = Subsection.objects.filter(section__in=sections)
        questions = Question.objects.filter(subsection__in=subsections)
        return render(request, 'formapp/form_score.html', {
            'form': form,
            'sections': sections,
            'subsections': subsections,
            'questions': questions,
        })
    elif request.method == 'POST':
        for question in Question.objects.filter(subsection__in=Subsection.objects.filter(section__in=Section.objects.filter(form=form))):
            score = request.POST.get(str(question.id))
            if score is not None and 0 <= int(score) <= 5:
                response, created = Response.objects.get_or_create(
                    assignment=FormAssignment.objects.get(form=form, employee=request.user.employee),
                    question=question,
                )
                response.score = int(score)
                response.save()
        return redirect('employee_dashboard')
