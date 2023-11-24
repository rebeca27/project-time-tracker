import argparse
from datetime import datetime, timedelta
from tracker import TimeTracker

def parse_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()

def parse_duration(duration_string):
    hours, minutes = map(int, duration_string.split(':'))
    return timedelta(hours=hours, minutes=minutes)

def main():
    parser = argparse.ArgumentParser(description='Time Tracker CLI')
    parser.add_argument('action', help='Action to perform', choices=['start', 'stop', 'pause', 'resume', 'report', 'export'])
    parser.add_argument('--project', help='Project name', required=False)
    parser.add_argument('--start_date', help='Start date for filtering (YYYY-MM-DD)', type=parse_date, required=False)
    parser.add_argument('--end_date', help='End date for filtering (YYYY-MM-DD)', type=parse_date, required=False)
    parser.add_argument('--min_duration', help='Minimum duration for filtering (HH:MM)', type=parse_duration, required=False)
    args = parser.parse_args()

    tracker = TimeTracker()

    if args.action == 'start':
        if args.project:
            tracker.start_tracking(args.project)
        else:
            print("Project name is required for starting a new tracking session.")

    elif args.action == 'stop':
        tracker.stop_tracking()

    elif args.action == 'pause':
        tracker.pause_tracking()

    elif args.action == 'resume':
        tracker.resume_tracking()

    elif args.action == 'report':
        base_file_name = 'project_report'
        
        if args.project:
            filtered_data = {args.project: tracker.filter_by_project(args.project)}
            file_name_suffix = f"_{args.project}"
        elif args.start_date and args.end_date:
            filtered_data = tracker.filter_by_date_range(args.start_date, args.end_date)
            file_name_suffix = f"_{args.start_date}_to_{args.end_date}"
        elif args.min_duration:
            filtered_data = tracker.filter_by_minimum_duration(args.min_duration)
            # Replace colons with another character like underscore or remove them
            min_duration_str = str(args.min_duration).replace(':', '_')
            file_name_suffix = f"_min_duration_{min_duration_str}"
        else:
            filtered_data = None
            file_name_suffix = ""

        report_file_name = f"{base_file_name}{file_name_suffix}.csv"
        report_file_name = 'project_report.csv'
        if filtered_data is not None:
            tracker.export_report_to_csv(report_file_name, filtered_projects=filtered_data)
        else:
            tracker.export_report_to_csv(report_file_name)



    elif args.action == 'export':
        tracker.export_to_csv()

if __name__ == '__main__':
    main()
