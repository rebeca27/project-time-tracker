import argparse
from tracker import TimeTracker

def main():
    parser = argparse.ArgumentParser(description='Time Tracker CLI')
    parser.add_argument('action', help='Action to perform', choices=['start', 'stop', 'pause', 'resume', 'report','export'])
    parser.add_argument('--project', help='Project name', required=False)
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
    elif args.action == 'stop':
        tracker.stop_tracking()
    elif args.action == 'report':
        tracker.report()
    elif args.action == 'export':
        tracker.export_to_csv()

if __name__ == '__main__':
    main()
