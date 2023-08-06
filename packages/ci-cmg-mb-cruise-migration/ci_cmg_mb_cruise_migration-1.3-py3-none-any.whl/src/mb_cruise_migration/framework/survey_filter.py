from src.mb_cruise_migration.framework.consts.nos_hydro_surveys import NosHydro
from src.mb_cruise_migration.framework.consts.survey_blacklist import SurveyBlacklist
from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.logging.migration_report import MigrationReport
from src.mb_cruise_migration.models.mb.mb_survey import MbSurvey


class SurveyFilter(object):
    @classmethod
    def filter(cls, surveys: [MbSurvey]):
        return [survey for survey in surveys if not cls.__filter_survey(survey)]

    @classmethod
    def __filter_survey(cls, survey: MbSurvey) -> bool:
        is_blacklisted = survey.survey_name in SurveyBlacklist.BLACKLIST
        if is_blacklisted:
            MigrationReport.add_skipped_survey(survey.survey_name)
            MigrationLog.log_skipped_survey(survey.survey_name, "survey was blacklisted for this migration run.")
            return is_blacklisted

        is_nos_hydro = survey.survey_name in NosHydro.SURVEYS
        if is_nos_hydro:
            MigrationReport.add_skipped_survey(survey.survey_name)
            MigrationLog.log_skipped_survey(survey.survey_name, "survey was an NOS Hydro survey that will not be migrated.")
            return is_nos_hydro
        return False
