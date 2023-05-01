# Django Recipe Manager

This is a web application built using Django framework that allows users to create, store, and manage their personal recipes.

## Installation and Usage

1. Clone the repository:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/jwobarros/django-recipe-manager.git
</code></div></div></pre>

2. Create a virtual environment and activate it:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">python3 -m venv env
source env/bin/activate
</code></div></div></pre>

3. Install the required packages:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install -r requirements.txt
</code></div></div></pre>

4. Set up the database:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">python manage.py makemigrations
python manage.py migrate
</code></div></div></pre>

5. Create a superuser:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">python manage.py createsuperuser
</code></div></div></pre>

6. Run the development server:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">python manage.py runserver
</code></div></div></pre>

7. Open your web browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You should now see the Recipe Manager Login page.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
