import datetime
import json
import os
import csv

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.pause_time = None
        self.current_project = None
        self.data_file = "timetracker_data.json"
        self.load_data()
   
    def start_tracking(self, project_name):
        if self.current_project and self.start_time:
            print(f"Already tracking project: {self.current_project}. Please stop before starting a new project.")
            return

        self.current_project = project_name
        self.start_time = datetime.datetime.now()

        if project_name not in self.projects:
            self.projects[project_name] = []
        
        self.save_data() 
        #print(f"Started tracking project: {self.current_project}")
        print(f"Started tracking project: {project_name}")


    def pause_tracking(self):
        self.load_data()  # Load the current state from file

        if not self.current_project or not self.start_time:
            print("No active project to pause.")
            return

        self.pause_time = datetime.datetime.now()
        elapsed = self.pause_time - self.start_time
        if self.current_project in self.projects:
            self.projects[self.current_project].append({
                "start": self.start_time.isoformat(),
                "end": self.pause_time.isoformat(),
                "duration": str(elapsed)
            })
        else:
            self.projects[self.current_project] = [{
                "start": self.start_time.isoformat(),
                "end": self.pause_time.isoformat(),
                "duration": str(elapsed)
            }]

        # Reset current_project and start_time after pausing
        self.current_project = None
        self.start_time = None
        self.save_data()
        print(f"Paused tracking project: {self.current_project}")


    def resume_tracking(self):
        if self.current_project and not self.start_time:
            self.start_time = datetime.datetime.now()
        else:
            print("No project is paused or an active project is already running.")
        print(f"Resumed tracking project: {self.current_project}")

    def stop_tracking(self):
        self.load_data()  # Load the current state from file

        if not self.current_project:
            print("No active project to stop.")
            return

        end_time = datetime.datetime.now()
        if self.start_time:
            elapsed = end_time - self.start_time
            if self.current_project in self.projects:
                self.projects[self.current_project].append({
                    "start": self.start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "duration": str(elapsed)
                })
            else:
                self.projects[self.current_project] = [{
                    "start": self.start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "duration": str(elapsed)
                }]

        # Reset current_project and start_time after stopping
        self.current_project = None
        self.start_time = None
        self.save_data()
     
    def export_report_to_csv(self, file_name='report.csv', filtered_projects=None):
        projects_to_export = filtered_projects if filtered_projects is not None else self.projects

        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Project', 'Start Time', 'End Time', 'Duration'])

            for project, entries in projects_to_export.items():
                total_duration = datetime.timedelta()
                for entry in entries:
                    start = datetime.datetime.fromisoformat(entry['start'])
                    end = datetime.datetime.fromisoformat(entry['end'])
                    duration = end - start
                    total_duration += duration
                    writer.writerow([project, start, end, duration])

                writer.writerow([f"Total for {project}", '', '', total_duration])

        print(f"Report exported to {file_name}")

    def report(self):
        for project, entries in self.projects.items():
            total_duration = datetime.timedelta()
            print(f"Project: {project}")
            for entry in entries:
                start = datetime.datetime.fromisoformat(entry['start'])
                end = datetime.datetime.fromisoformat(entry['end'])
                duration = end - start
                total_duration += duration
                print(f"  Start: {start}, End: {end}, Duration: {duration}")
            print(f"Total time spent: {total_duration}")

        
    def save_data(self):
        data = {
        'projects': self.projects,
        'current_project': self.current_project,
        'start_time': self.start_time.isoformat() if self.start_time else None
    }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)
        print("Data saved.")

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.projects = data.get('projects', {})
                self.current_project = data.get('current_project')
                self.start_time = datetime.datetime.fromisoformat(data['start_time']) if data.get('start_time') else None
        else:
            self.projects = {}
        print("Data loaded.")


    def filter_by_project(self, project_name):
        if project_name in self.projects:
            return self.projects[project_name]
        else:
            print(f"No data found for project: {project_name}")
            return []

    def filter_by_date_range(self, start_date, end_date):
        filtered_data = {}
        for project, entries in self.projects.items():
            filtered_entries = []
            for entry in entries:
                entry_date = datetime.datetime.fromisoformat(entry['start']).date()
                if start_date <= entry_date <= end_date:
                    filtered_entries.append(entry)
            if filtered_entries:
                filtered_data[project] = filtered_entries
        return filtered_data

    def filter_by_minimum_duration(self, min_duration):
        filtered_data = {}
        for project, entries in self.projects.items():
            filtered_entries = []
            for entry in entries:
                duration = datetime.datetime.fromisoformat(entry['end']) - datetime.datetime.fromisoformat(entry['start'])
                if duration >= min_duration:
                    filtered_entries.append(entry)
            if filtered_entries:
                filtered_data[project] = filtered_entries
        return filtered_data

    def export_to_csv(self, file_name='report.csv'):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Project', 'Start Time', 'End Time', 'Duration'])

            for project, entries in self.projects.items():
                for entry in entries:
                    writer.writerow([project, entry['start'], entry['end'], entry['duration']])
        print("Data exported.")
