from flask import jsonify
from data.jobs import Jobs
from data import db_session
from flask_restful import Resource
from pars_jobs import parser
from flask_restful import abort

db_session.global_init("db/blogs.db")


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('team_leader', 'job', 'collaborators', 'work_size', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
    

class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'collaborators', 'work_size', 'start_date', 'end_date', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            collaborators=args['collaborators'],
            work_size=args['work_size'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished'],
        )
        session.add(jobs)
        session.commit()
        return jsonify({'id': jobs.id})