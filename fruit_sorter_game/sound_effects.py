import pygame
import os
import numpy as np

class SoundEffects:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Sound effect dictionary
        self.sounds = {}
        
        # Default volume settings - lower volume to make less irritating
        self.sfx_volume = 0.4
        
        # Create sound directory if it doesn't exist
        sounds_dir = os.path.join("assets", "sounds")
        os.makedirs(sounds_dir, exist_ok=True)
        
        # Create enhanced sound effects
        self.create_enhanced_sounds()
    
    def create_enhanced_sounds(self):
        """Create improved sound effects for different game events"""
        # Define sound types
        sound_types = [
            "correct",
            "wrong",
            "bomb",
            "miss",
            "spawn_bomb",
            "game_over"
        ]
        
        # Create a sound for each type
        for sound_type in sound_types:
            if sound_type == "correct":
                # Pleasant ascending arpeggio
                self.sounds[sound_type] = self.create_arpeggio([440, 550, 660], 80, "up")
            elif sound_type == "wrong":
                # Descending minor notes
                self.sounds[sound_type] = self.create_arpeggio([330, 277, 220], 80, "down")
            elif sound_type == "bomb":
                # Explosion sound
                self.sounds[sound_type] = self.create_explosion_sound()
            elif sound_type == "miss":
                # Quick descending note
                self.sounds[sound_type] = self.create_sweep(440, 220, 150)
            elif sound_type == "spawn_bomb":
                # Warning sound
                self.sounds[sound_type] = self.create_warning_sound()
            elif sound_type == "game_over":
                # Game over chord
                self.sounds[sound_type] = self.create_chord([220, 277, 330], 500)
    
    def create_sine_wave(self, frequency, duration, volume=0.5):
        """Create a sine wave array for a tone with fade in/out"""
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate / 1000))
        
        # Generate time array
        t = np.linspace(0, duration/1000, n_samples, False)
        
        # Generate sine wave
        note = np.sin(2 * np.pi * frequency * t)
        
        # Apply fade in and fade out
        fade_samples = int(n_samples * 0.1)  # 10% fade in/out
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        # Apply fades
        note[:fade_samples] *= fade_in
        note[-fade_samples:] *= fade_out
        
        # Apply volume
        note = note * volume
        
        # Convert to 16-bit signed integers
        note = (note * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo = np.column_stack((note, note))
        
        return stereo
    
    def create_arpeggio(self, frequencies, note_duration, direction="up"):
        """Create an arpeggio of notes"""
        sample_rate = 44100
        total_duration = note_duration * len(frequencies)
        n_samples = int(round(total_duration * sample_rate / 1000))
        
        # Create empty array
        arpeggio = np.zeros(n_samples, dtype=np.float32)
        
        # Generate each note
        for i, freq in enumerate(frequencies):
            # Calculate start position
            start_sample = i * int(round(note_duration * sample_rate / 1000))
            end_sample = start_sample + int(round(note_duration * sample_rate / 1000))
            
            # Generate time array for this note
            t = np.linspace(0, note_duration/1000, end_sample - start_sample, False)
            
            # Generate note
            note = np.sin(2 * np.pi * freq * t)
            
            # Apply fade in and fade out
            fade_samples = int((end_sample - start_sample) * 0.2)  # 20% fade in/out
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            # Apply fades
            note[:fade_samples] *= fade_in
            note[-fade_samples:] *= fade_out
            
            # Add to arpeggio
            arpeggio[start_sample:end_sample] = note
        
        # Apply volume
        arpeggio = arpeggio * 0.7
        
        # Convert to 16-bit signed integers
        arpeggio = (arpeggio * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo = np.column_stack((arpeggio, arpeggio))
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(stereo)
        return sound
    
    def create_sweep(self, start_freq, end_freq, duration, volume=0.5):
        """Create a frequency sweep"""
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate / 1000))
        
        # Generate time array
        t = np.linspace(0, duration/1000, n_samples, False)
        
        # Generate logarithmic frequency sweep
        freq = np.exp(np.linspace(np.log(start_freq), np.log(end_freq), n_samples))
        
        # Generate phase by integrating frequency
        phase = np.cumsum(2 * np.pi * freq / sample_rate)
        
        # Generate sweep
        sweep = np.sin(phase)
        
        # Apply fade in and fade out
        fade_samples = int(n_samples * 0.1)  # 10% fade in/out
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        # Apply fades
        sweep[:fade_samples] *= fade_in
        sweep[-fade_samples:] *= fade_out
        
        # Apply volume
        sweep = sweep * volume
        
        # Convert to 16-bit signed integers
        sweep = (sweep * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo = np.column_stack((sweep, sweep))
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(stereo)
        return sound
    
    def create_explosion_sound(self):
        """Create an explosion sound effect"""
        sample_rate = 44100
        duration = 300  # ms
        n_samples = int(round(duration * sample_rate / 1000))
        
        # Generate noise
        noise = np.random.uniform(-1, 1, n_samples)
        
        # Apply envelope
        envelope = np.exp(-np.linspace(0, 10, n_samples))
        explosion = noise * envelope
        
        # Apply low-pass filter (simple moving average)
        window_size = 10
        explosion = np.convolve(explosion, np.ones(window_size)/window_size, mode='same')
        
        # Apply volume
        explosion = explosion * 0.7
        
        # Convert to 16-bit signed integers
        explosion = (explosion * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo = np.column_stack((explosion, explosion))
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(stereo)
        return sound
    
    def create_warning_sound(self):
        """Create a warning sound effect"""
        sample_rate = 44100
        beep_duration = 100  # ms
        gap_duration = 50  # ms
        n_beeps = 2
        
        total_duration = n_beeps * beep_duration + (n_beeps - 1) * gap_duration
        n_samples = int(round(total_duration * sample_rate / 1000))
        
        # Create empty array
        warning = np.zeros(n_samples, dtype=np.float32)
        
        # Generate beeps
        for i in range(n_beeps):
            # Calculate start position
            start_sample = i * int(round((beep_duration + gap_duration) * sample_rate / 1000))
            end_sample = start_sample + int(round(beep_duration * sample_rate / 1000))
            
            # Generate time array for this beep
            t = np.linspace(0, beep_duration/1000, end_sample - start_sample, False)
            
            # Generate beep (use square wave for harsher sound)
            beep = np.sign(np.sin(2 * np.pi * 440 * t))
            
            # Apply fade in and fade out
            fade_samples = int((end_sample - start_sample) * 0.2)  # 20% fade in/out
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            # Apply fades
            beep[:fade_samples] *= fade_in
            beep[-fade_samples:] *= fade_out
            
            # Add to warning
            warning[start_sample:end_sample] = beep
        
        # Apply volume
        warning = warning * 0.5
        
        # Convert to 16-bit signed integers
        warning = (warning * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo = np.column_stack((warning, warning))
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(stereo)
        return sound
    
    def create_chord(self, frequencies, duration, volume=0.5):
        """Create a chord with multiple frequencies"""
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate / 1000))
        
        # Generate time array
        t = np.linspace(0, duration/1000, n_samples, False)
        
        # Create empty array
        chord = np.zeros(n_samples, dtype=np.float32)
        
        # Add each frequency component
        for freq in frequencies:
            chord += np.sin(2 * np.pi * freq * t)
        
        # Normalize
        chord = chord / len(frequencies)
        
        # Apply fade in and fade out
        fade_samples = int(n_samples * 0.2)  # 20% fade in/out
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        # Apply fades
        chord[:fade_samples] *= fade_in
        chord[-fade_samples:] *= fade_out
        
        # Apply volume
        chord = chord * volume
        
        # Convert to 16-bit signed integers
        chord = (chord * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo = np.column_stack((chord, chord))
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(stereo)
        return sound
    
    def play(self, sound_name):
        """Play a sound effect by name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sfx_volume)
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found")
    
    def set_volume(self, volume):
        """Set volume for all sound effects (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def stop_all(self):
        """Stop all currently playing sound effects"""
        pygame.mixer.stop()
