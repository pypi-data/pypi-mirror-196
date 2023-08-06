from ververser.update_timer import UpdateTimer


class UpdateStepper:

    def __init__( self, frame_time, max_updates = 5 ):
        self.frame_time = frame_time
        self.max_updates = max_updates

        self.update_timer = UpdateTimer()
        self.remaining_time_to_consume = 0
        self.n_updates = 0

    def produce( self ) -> None:
        # measure the time that has passed since last frame,
        # this is basically time that we have to consume by running game updates
        dt = self.update_timer.restart()
        self.remaining_time_to_consume += dt
        self.n_updates = 0

    def consume( self ) -> bool:
        # consume time by running game updates
        # we choose to use fixed size timesteps because they result in more stable physics
        # you want limit the number of consecutive updates in case you used a breakpoint,
        # and to prevent situations where your application might otherwise never catch up
        has_time_to_consume = self.remaining_time_to_consume >= self.frame_time
        has_steps_to_consume = self.n_updates < self.max_updates
        can_step = has_time_to_consume and has_steps_to_consume
        if can_step:
            self.remaining_time_to_consume -= self.frame_time
            self.n_updates += 1
            return True
        return False
