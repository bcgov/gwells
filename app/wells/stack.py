from wells.models import ActivitySubmission


class StackWells():

    def create(self, filing_number):
        # Take a submission, and use it to create a well entry
        submission = ActivitySubmission.objects.get(filing_number=filing_number)
        well_data = None
        if submission.well_tag_number is not None:
            logger.info('Submission {} already has a well tag number {}'.format(
                filing_number, submission.well_tag_number))
            self.update_well_record(well_data, submission.well_tag_number)

    def stack(self, well_tag_number):
        # Get all submissions for a particular well.
        submissions = ActivitySubmission.objects.filter(well_tag_number=well_tag_number)

        # Iterate through them, stacking them.

        # Store the result.

    def _insert_well_record(self):
        pass

    def _update_well_record(self):
        pass
