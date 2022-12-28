from django.views.generic import (ListView, CreateView, UpdateView,DeleteView)
from .models import ToDoList,ToDoItem
from django.urls import reverse, reverse_lazy
#this is like the guide for what html file to load for different rotutes
class ListDelete(DeleteView):
    model=ToDoList
    #have to use reverse lazy bc urls are not
    #loaded when file is imported
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model=ToDoItem
    def get_success_url(self) -> str:
        return reverse_lazy("list",args=[self.kwargs["list_id"]])
    
    def get_context_data(self, **kwargs: any):
        context= super().get_context_data(**kwargs)
        context["todo_list"]=self.object.todo_list
        return context
#this is to view multiple lists as a list
class ListListView(ListView):
    model=ToDoList
    template_name="todo_app/index.html"

#list items in a to do list
class ItemListView(ListView):
    model = ToDoItem
    template_name="todo_app/todo_list.html"

    #get items whose ids match the list id
    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    #context is a python dictioanry that determines what data can be rendered
    def get_context_data(self):
        context= super().get_context_data() #gets the dictioanry of all objects returned by query set - a bunch of seperate objects
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class ListCreate(CreateView):
    #using to do list model(db)
    model=ToDoList
    #one field that is public for user to change. Field is a dictionary that can be changed like a form
    fields= ["title"]

    #function to get form data
    def get_context_data(self):
        #context(form that we are using to create list) uses the super class for context
        context= super(ListCreate,self).get_context_data()
        #context has a title
        context["title"]="Add a new list"
        return context

class ItemCreate(CreateView):
    #new item is using the item model. Has four fields that can be changed / four keys in its dictionary
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    #get initial data for a new item
    def get_initial(self):
        initial_data=super(ItemCreate,self).get_initial()
        todo_list=ToDoList.objects.get(id=self.kwargs["list_id"]) #to do list is the set of objects whose list id matches self.listid
        initial_data["todo_list"]=todo_list 
        return initial_data
    
    #create a form for item creation
    def get_context_data(self):
        context= super(ItemCreate,self).get_context_data() #basic form
        todo_list=ToDoList.objects.get(id=self.kwargs["list_id"]) #to do list is the set of objects whose list id matches self.listid
        context["todo_list"]=todo_list 
        context["title"] = "Create a new item"
        return context
    #after new item created heres what the view is
    def get_success_url(self) -> str:
        return reverse("list",args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model=ToDoItem
    fields=[
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context= super(ItemUpdate, self).get_context_data()
        context["todo_list"]=self.object.todo_list
        context["title"] = "edit item"
        return context
    def get_success_url(self):
        return reverse("list",args=[self.object.todo_list_id])



