import logging
from pathlib import Path
from typing import Optional

import pyglet

from ververser.content_manager import ContentManager, LoadStatus
from ververser.fps_counter import FPSCounter
from ververser.keyboard import Keyboard
from ververser.main_script import MainScript
from ververser.mouse import Mouse
from ververser.update_stepper import UpdateStepper


logger = logging.getLogger(__name__)


class GameWindow( pyglet.window.Window ):

    def __init__( self, content_folder_path : Path, throttle_fps = 60, **kwargs ):
        super().__init__( vsync = False, **kwargs )

        self.target_fps = throttle_fps
        self.fps_counter = FPSCounter()
        self.frame_time = 1 / self.target_fps
        self.update_stepper = UpdateStepper( frame_time = self.frame_time )

        self.alive = True
        self.is_paused = False
        self.requires_init = True
        self.has_init_problem = False
        self.has_content_problem = False

        self.content_manager = ContentManager( content_folder_path )
        self.main_script : Optional[ MainScript ] = None

        self.keyboard = Keyboard()
        self.push_handlers( self.keyboard.get_handler() )

        self.mouse = Mouse()
        self.push_handlers( self.mouse.get_handler() )

    # ================ Events ================
    def on_draw(self, dt):
        self.draw()

    # ================ State affectors ================

    def on_close(self) -> None:
        self.alive = False

    def quit( self ) -> None:
        self.alive = False

    def restart( self ) -> None:
        self.requires_init = True

    # ================ Run game loop ================

    def run(self) -> None:
        while self.alive:
            # dispatch all OS events
            self.dispatch_events()

            # if there was a problem with initialisation and no content was modified yet,
            # then there is no need to retry initialisation.
            # Note that it can happen that a script initializer throws an error, because of an asset issue.
            # That's why we also check for updated assets here, and not only scripts.
            is_any_script_updated = self.content_manager.is_any_script_updated()
            is_any_asset_updated = self.content_manager.is_any_asset_updated()
            is_any_content_updated = is_any_script_updated or is_any_asset_updated
            if self.has_init_problem and not is_any_content_updated:
                continue

            # if any script files are updated we require reinitialisation
            if is_any_script_updated:
                self.exit()
                self.requires_init = True

            # try to initialise the game
            # if a problem is encountered, then end the frame early
            if self.requires_init:
                self._init()
                if self.has_init_problem:
                    continue

            # by now we know our scripts are properly initialised

            # Now that scripts have been handled,
            # we will try to reload assets (which is done only if they have been modified)
            reload_status = self.content_manager.try_reload_assets()
            if reload_status == LoadStatus.FAILED :
                logger.info( "Error occured during asset loading. Game is now paused!" )
                self.has_content_problem = True
                continue
            else :
                if reload_status == LoadStatus.RELOADED :
                    self.has_content_problem = False

            if self.is_paused or self.has_content_problem:
                continue

            # by this point we have accepted the game should just continue running normally
            # during update and draw we might still encounter problems
            # we do not know necessarily if those are caused by scripts or assets,
            # so we just call them content problems

            self.update_stepper.produce()
            while self.update_stepper.consume():
                self._update(self.frame_time)
                self.update(self.frame_time)

                self._draw_start()
                self.draw()
                self._draw_end()

        self.exit()

    # ---------------- Functions that wrap standard game hooks  ----------------

    def _init( self ) -> None:
        success = self.try_invoke( self.init, 'Game Init' )
        if not success:
            self.has_init_problem = True
        else:
            self.has_init_problem = False
            self.requires_init = False
            self.has_content_problem = False

    def _update( self, dt ) -> None:
        self.fps_counter.update()

    def _draw_start( self ) -> None:
        self.clear()

    def _draw_end( self ) -> None:
        self.fps_counter.draw()
        self.flip()

    # ---------------- Convenience Functions ----------------
    def try_invoke( self, f, current_task : str ) -> bool:
        success = True
        try :
            f()
        except BaseException as e:
            logger.exception( f'Caught an Exception: {e}' )
            logger.error( f'∧∧∧ Error occurred during {current_task}. Game is now paused! ∧∧∧' )
            success = False
        return success

    # ================ End of standard boilerplate ================
    # ================ Overload the methods below! ================

    def init( self ) -> None:
        self.content_manager.script_watcher.clear()
        self.main_script = self.content_manager.load_main_script( self )
        assert self.main_script

    def update( self, dt ) -> None:
        was_update_successful = self.try_invoke( lambda : self.main_script.vvs_update( dt ), 'Game Update' )
        if not was_update_successful:
            self.has_content_problem = True

    def draw( self ) -> None:
        was_draw_successful = self.try_invoke( self.main_script.vvs_draw, 'Game Draw' )
        if not was_draw_successful :
            self.has_content_problem = True

    def exit( self ):
        if not self.main_script:
            return
        try :
            self.main_script.vvs_exit()
        except BaseException as e:
            logger.exception( f'Caught an Exception: {e}' )
            logger.error( f'∧∧∧ Error occurred during Game Exit. Game will be reinitialized, but your state will be lost ∧∧∧' )
