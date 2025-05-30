import pygame
import numpy as np
import os

class BackgroundMusic:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        
        # Create music directory if it doesn't exist
        music_dir = os.path.join("assets", "music")
        os.makedirs(music_dir, exist_ok=True)
        
        # Set up music channels
        self.music_channel = pygame.mixer.Channel(7)  # Reserve channel 7 for music
        self.volume = 0.4
        
        # Music file path
        self.music_path = os.path.join(music_dir, "space_theme.ogg")
        
        # Load music - use the existing file without trying to generate a new one
        try:
            print(f"Loading music from {self.music_path}")
            self.music = pygame.mixer.Sound(self.music_path)
            self.music.set_volume(self.volume)
            print("Music loaded successfully!")
        except Exception as e:
            print(f"Error loading music: {e}")
            print("Generating fallback music")
            self.music = self.generate_simple_loop()
            self.music.set_volume(self.volume)
    
    def generate_space_theme(self):
        """Generate a Star Wars-themed background music loop"""
        try:
            # This is a placeholder - in a real implementation, we would
            # generate a more complex music file. For now, we'll create
            # a Star Wars inspired loop and save it.
            self.generate_simple_loop(save_path=self.music_path)
            print(f"Generated music saved to {self.music_path}")
        except Exception as e:
            print(f"Error generating music: {e}")
    
    def generate_simple_loop(self, save_path=None):
        """Generate a Star Wars-themed music loop"""
        # Parameters
        sample_rate = 44100
        duration = 10.0  # 10 second loop
        bpm = 120  # Imperial March tempo
        
        # Calculate total samples
        total_samples = int(sample_rate * duration)
        
        # Create empty array for the loop
        music_data = np.zeros((total_samples, 2), dtype=np.float32)
        
        # Define a Star Wars-inspired chord progression (Imperial March inspired)
        chords = [
            [146.83, 220.00, 293.66],  # D minor
            [130.81, 196.00, 261.63],  # C minor
            [146.83, 220.00, 293.66],  # D minor
            [116.54, 174.61, 233.08]   # Bb major
        ]
        
        # Define a Star Wars-inspired bassline (Imperial March motif)
        bassline = [73.42, 73.42, 73.42, 58.27, 87.31, 73.42, 58.27, 87.31, 73.42]  # D, D, D, Bb, F, D, Bb, F, D
        
        # Calculate samples per beat and per chord
        samples_per_beat = int(60.0 / bpm * sample_rate)
        samples_per_chord = samples_per_beat * 4  # 4 beats per chord
        
        # Generate each chord
        for i, chord in enumerate(chords):
            # Calculate start and end samples for this chord
            start_sample = i * samples_per_chord
            end_sample = start_sample + samples_per_chord
            
            if end_sample > total_samples:
                end_sample = total_samples
            
            # Generate time array for this chord
            t = np.linspace(0, (end_sample - start_sample) / sample_rate, end_sample - start_sample, False)
            
            # Generate chord tones with a sci-fi synth sound
            chord_data = np.zeros_like(t)
            for note in chord:
                # Add sine wave for each note in the chord
                chord_data += 0.15 * np.sin(2 * np.pi * note * t)
                # Add a bit of the first harmonic
                chord_data += 0.05 * np.sin(2 * np.pi * note * 2 * t)
                # Add some detuned oscillators for thickness
                chord_data += 0.05 * np.sin(2 * np.pi * (note * 1.01) * t)
            
            # Add some noise for texture
            noise = np.random.uniform(-0.02, 0.02, len(t))
            chord_data += noise
            
            # Normalize
            chord_data = chord_data / len(chord)
            
            # Apply envelope
            envelope = np.ones_like(t)
            attack = int(0.1 * samples_per_chord)  # 10% attack
            decay = int(0.2 * samples_per_chord)   # 20% decay
            release = int(0.3 * samples_per_chord) # 30% release
            
            # Attack
            envelope[:attack] = np.linspace(0, 1, attack)
            # Decay
            envelope[attack:attack+decay] = np.linspace(1, 0.7, decay)
            # Release
            release_start = len(envelope) - release
            if release_start > 0:
                envelope[release_start:] = np.linspace(0.7, 0.2, release)
            
            # Apply envelope
            chord_data = chord_data * envelope
            
            # Add to music data (left channel)
            music_data[start_sample:end_sample, 0] += chord_data * 0.7
            
            # Generate bassline with a deeper, more resonant sound
            bass_note = bassline[i]
            bass_data = 0.3 * np.sin(2 * np.pi * bass_note * t)
            
            # Add some harmonics for richer bass
            bass_data += 0.15 * np.sin(2 * np.pi * bass_note * 2 * t)
            bass_data += 0.05 * np.sin(2 * np.pi * bass_note * 3 * t)
            
            # Add some filter sweep effect
            filter_sweep = np.linspace(0.5, 1.0, len(t))
            bass_data *= filter_sweep
            
            # Create bass envelope (punchier)
            bass_env = np.ones_like(t)
            bass_attack = int(0.05 * samples_per_chord)  # 5% attack
            bass_decay = int(0.3 * samples_per_chord)    # 30% decay
            
            # Bass attack
            bass_env[:bass_attack] = np.linspace(0, 1, bass_attack)
            # Bass decay
            bass_env[bass_attack:bass_attack+bass_decay] = np.linspace(1, 0.3, bass_decay)
            
            # Apply bass envelope
            bass_data = bass_data * bass_env
            
            # Add to music data (both channels, but stronger in right)
            music_data[start_sample:end_sample, 0] += bass_data * 0.5
            music_data[start_sample:end_sample, 1] += bass_data * 0.8
            
            # Add some space-themed arpeggios
            for j in range(8):  # 8 eighth notes per chord
                beat_start = start_sample + j * (samples_per_beat // 2)
                beat_end = beat_start + (samples_per_beat // 2)
                
                if beat_end > total_samples:
                    beat_end = total_samples
                
                # Skip if we're out of bounds
                if beat_start >= total_samples:
                    continue
                
                # Generate time array for this beat
                beat_t = np.linspace(0, (beat_end - beat_start) / sample_rate, beat_end - beat_start, False)
                
                # Choose a note from the chord for the arpeggio
                arp_note = chord[j % len(chord)]
                
                # For sci-fi feel, use a square wave with some filtering
                arp_data = 0.1 * np.sign(np.sin(2 * np.pi * arp_note * beat_t))
                
                # Apply low-pass filter (simple moving average)
                window_size = 5
                arp_data = np.convolve(arp_data, np.ones(window_size)/window_size, mode='same')
                
                # Create arpeggio envelope
                arp_env = np.ones_like(beat_t)
                arp_attack = int(0.1 * len(beat_t))  # 10% attack
                arp_release = int(0.7 * len(beat_t)) # 70% release
                
                # Arpeggio attack
                if arp_attack > 0:
                    arp_env[:arp_attack] = np.linspace(0, 1, arp_attack)
                # Arpeggio release
                arp_release_start = len(arp_env) - arp_release
                if arp_release_start > 0:
                    arp_env[arp_release_start:] = np.linspace(1, 0, arp_release)
                
                # Apply arpeggio envelope
                arp_data = arp_data * arp_env
                
                # Add to music data (right channel)
                if beat_start + len(arp_data) <= total_samples:
                    music_data[beat_start:beat_start+len(arp_data), 1] += arp_data
        
        # Add some space-themed percussion
        for i in range(0, total_samples, samples_per_beat):
            # Skip if we're out of bounds
            if i + 1000 > total_samples:
                continue
            
            # Every 4 beats, add a "whoosh" sound
            if (i // samples_per_beat) % 4 == 0:
                whoosh_len = samples_per_beat
                if i + whoosh_len > total_samples:
                    whoosh_len = total_samples - i
                
                # Create a filtered noise sweep
                noise = np.random.uniform(-0.1, 0.1, whoosh_len)
                
                # Apply envelope
                env = np.exp(-np.linspace(0, 5, whoosh_len))
                noise = noise * env
                
                # Apply filter sweep
                for j in range(whoosh_len):
                    cutoff = 0.1 + 0.8 * (1 - j/whoosh_len)
                    if j > 0:
                        noise[j] = noise[j] * cutoff + noise[j-1] * (1-cutoff)
                
                # Add to both channels
                music_data[i:i+whoosh_len, 0] += noise * 0.2
                music_data[i:i+whoosh_len, 1] += noise * 0.2
            
            # Every beat, add a subtle "click"
            click_len = 100
            if i + click_len <= total_samples:
                click = np.random.uniform(-0.1, 0.1, click_len)
                click_env = np.exp(-np.linspace(0, 10, click_len))
                click = click * click_env
                
                music_data[i:i+click_len, 0] += click * 0.1
                music_data[i:i+click_len, 1] += click * 0.1
        
        # Normalize
        max_val = np.max(np.abs(music_data))
        if max_val > 0:
            music_data = music_data / max_val * 0.9
        
        # Convert to 16-bit signed integers
        music_data = (music_data * 32767).astype(np.int16)
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(music_data)
        
        # Save if path is provided
        if save_path:
            try:
                pygame.mixer.Sound.save(sound, save_path)
            except:
                print(f"Could not save music to {save_path}")
        
        return sound
    
    def play(self):
        """Play the background music on loop"""
        self.music_channel.play(self.music, loops=-1)
    
    def stop(self):
        """Stop the background music"""
        self.music_channel.stop()
    
    def set_volume(self, volume):
        """Set the volume of the background music"""
        self.volume = max(0.0, min(1.0, volume))
        self.music.set_volume(self.volume)
    
    def fade_in(self, milliseconds=2000):
        """Fade in the music"""
        # Start at zero volume
        self.music.set_volume(0)
        self.music_channel.play(self.music, loops=-1)
        
        # Create a timer to gradually increase volume
        self.fade_steps = 20
        self.fade_amount = self.volume / self.fade_steps
        self.fade_delay = milliseconds / self.fade_steps
        self.current_fade_step = 0
        
        # Start the fade timer
        pygame.time.set_timer(pygame.USEREVENT + 1, int(self.fade_delay))
    
    def update_fade(self):
        """Update the fade-in effect"""
        if self.current_fade_step < self.fade_steps:
            self.current_fade_step += 1
            new_volume = self.current_fade_step * self.fade_amount
            self.music.set_volume(new_volume)
        else:
            # Stop the timer when fade is complete
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
    
    def fade_out(self, milliseconds=2000):
        """Fade out the music"""
        # Create a timer to gradually decrease volume
        self.fade_steps = 20
        self.fade_amount = self.volume / self.fade_steps
        self.fade_delay = milliseconds / self.fade_steps
        self.current_fade_step = self.fade_steps
        
        # Start the fade timer
        pygame.time.set_timer(pygame.USEREVENT + 2, int(self.fade_delay))
    
    def update_fade_out(self):
        """Update the fade-out effect"""
        if self.current_fade_step > 0:
            self.current_fade_step -= 1
            new_volume = self.current_fade_step * self.fade_amount
            self.music.set_volume(new_volume)
        else:
            # Stop the timer and the music when fade is complete
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            self.music_channel.stop()
