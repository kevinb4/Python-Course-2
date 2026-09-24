# Python Course 2

A second, more advanced Python course project built around progressively bigger weekly assignments. From OOP and functions, through automated testing, to two full CRUD applications backed by a MySQL/MariaDB database, culminating in a capstone project that ties everything together.

## Structure

<dl>
<dt><strong>Week 1-2: Classes &amp; Functions</strong></dt>
<dd>Introductory OOP and functions exercises.</dd>

<dt><strong>Week 3-4: Config Manager</strong></dt>
<dd>A CLI tool that loads app settings from a basic_config.json file and lets the user view, add, and modify/remove entries through a menu. Changes can optionally be saved to a config_override.json file, which takes precedence over the defaults on future runs. Includes required-field validation and a save/discard confirmation prompt.</dd>

<dt><strong>Week 5-6: Testing Your Code</strong></dt>
<dd>Introduces automated testing of the codebase using Python's unittest framework.</dd>

<dt><strong>Week 7-9: Vehicle Dealership App</strong></dt>
<dd>A CLI application for managing a dealership's vehicle inventory, connected to a MariaDB/MySQL database via a DB_Connect class (built on pymysql) that wraps connection handling and query execution. Supports full CRUD on a vehicle table - listing (short and detailed views), adding a vehicle (make, model, VIN, optional previous owner/price paid, sale price, description), editing any field, and removing a vehicle. All input is validated per field (alphanumeric VIN, float pricing, allowed/disallowed character sets for names) and all queries use parameterized SQL to prevent injection.</dd>

<dt><strong>Week 10: Customer Import &amp; CRM System (Final Project)</strong></dt>
<dd>A CLI application that imports customer data from a pipe-delimited text file export, deduplicates it by email, and distributes it across two MySQL tables (crm_data and mailings) using the same DB_Connect class from Week 7. It includes an import pipeline that parses the raw export, writes CSV/JSON backups, and bulk-loads both database tables in single batched queries; full CRUD across both tables with prompts and validation that adapt to the selected table; per-field validation for names, addresses, city, state, zip, phone, and email; automated tests (unittest) covering valid/invalid customer creation and formatting helpers; and auto-generated documentation for the functions, classes, and test modules.</dd>
</dl>

## Tech Stack
- Python 3
- MySQL / MariaDB (`pymysql`)
- `unittest` for testing
- `json`, `csv` for data import/export
