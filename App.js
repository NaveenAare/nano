
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Image, ScrollView, ActivityIndicator, SafeAreaView, KeyboardAvoidingView, Platform, Animated, Easing } from 'react-native';
import { StatusBar } from 'expo-status-bar';

// Simulated Auth Session for now until we configure Google Cloud Console
export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  
  // Animation Values
  const spinValue = new Animated.Value(0);
  const floatValue = new Animated.Value(0);
  const fadeValue = new Animated.Value(0);

  useEffect(() => {
    // Background spin animation
    Animated.loop(
      Animated.timing(spinValue, {
        toValue: 1,
        duration: 20000,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    ).start();

    // Floating logo animation
    Animated.loop(
      Animated.sequence([
        Animated.timing(floatValue, { toValue: 1, duration: 2000, useNativeDriver: true }),
        Animated.timing(floatValue, { toValue: 0, duration: 2000, useNativeDriver: true }),
      ])
    ).start();

    // Fade in text
    Animated.timing(fadeValue, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();
  }, []);

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg']
  });

  const translateY = floatValue.interpolate({
    inputRange: [0, 1],
    outputRange: [0, -15]
  });

  const handleLogin = () => {
    // In production, this will trigger expo-auth-session
    setIsAuthenticated(true);
  };

  const generateImage = async () => {
    if (!prompt.trim()) return;
    setIsGenerating(true);
    
    try {
      const formData = new FormData();
      formData.append('chat_id', 'bXYwNi1zZGtkZ3Y');
      formData.append('message', prompt);
      formData.append('does_chat_have_name', 'false');
      formData.append('models', 'ChatGpt');
      formData.append('versions_data', '[{"modelName":"ChatGpt","version":"gpt-3.5-turbo"}]');
      formData.append('requestId', `req_${Date.now()}`);
      
      const response = await fetch('https://chatezzy.com/chat/v2/nanobanana-direct', {
        method: 'POST',
        headers: {
          'Accept': '*/*',
          'Origin': 'https://chatezzy.com',
          'Referer': 'https://chatezzy.com/superai/bXYwNi1zZGtkZ3Y',
          'User-Agent': 'NanoBananaAndroid/1.0',
        },
        body: formData
      });
      
      const data = await response.json();
      if (data && typeof data === 'object') {
        const lastKey = Object.keys(data).pop();
        const finalChunk = data[lastKey];
        if (finalChunk && finalChunk.images && finalChunk.images.length > 0) {
          setGeneratedImage(finalChunk.images[0]);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  // --- LOGIN SCREEN ---
  if (!isAuthenticated) {
    return (
      <View style={styles.loginContainer}>
        <StatusBar style="light" />
        
        {/* Animated 3D Background Elements */}
        <Animated.View style={[styles.bgBlob, styles.blob1, { transform: [{ rotate: spin }] }]} />
        <Animated.View style={[styles.bgBlob, styles.blob2, { transform: [{ rotate: spin }] }]} />
        
        <View style={styles.loginContent}>
          <Animated.View style={[styles.logoContainer, { transform: [{ translateY }] }]}>
            <Text style={styles.logoEmoji}>🍌</Text>
          </Animated.View>
          
          <Animated.Text style={[styles.loginTitle, { opacity: fadeValue }]}>Nano Banana</Text>
          <Animated.Text style={[styles.loginSubtitle, { opacity: fadeValue }]}>Masterpiece Generation, Instantly.</Animated.Text>
          
          <TouchableOpacity style={styles.googleButton} onPress={handleLogin} activeOpacity={0.8}>
            <Image 
              source={{ uri: 'https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg' }} 
              style={styles.googleIcon} 
            />
            <Text style={styles.googleButtonText}>Continue with Google</Text>
          </TouchableOpacity>
          
          <Text style={styles.loginTerms}>By continuing, you agree to our Terms of Service</Text>
        </View>
      </View>
    );
  }

  // --- MAIN STUDIO SCREEN ---
  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="light" />
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Studio</Text>
          <TouchableOpacity onPress={() => setIsAuthenticated(false)}>
            <Image source={{ uri: 'https://ui-avatars.com/api/?name=User&background=f59e0b&color=000' }} style={styles.profilePic} />
          </TouchableOpacity>
        </View>

        <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
          <View style={styles.canvasContainer}>
            {isGenerating ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#f59e0b" />
                <Text style={styles.loadingText}>Rendering 4K Details...</Text>
              </View>
            ) : generatedImage ? (
              <Image source={{ uri: generatedImage }} style={styles.generatedImage} resizeMode="cover" />
            ) : (
              <View style={styles.placeholderContainer}>
                <Text style={styles.placeholderIcon}>✨</Text>
                <Text style={styles.placeholderText}>Describe your masterpiece...</Text>
              </View>
            )}
          </View>
        </ScrollView>

        <View style={styles.inputDock}>
          <TextInput
            style={styles.input}
            placeholder="Type a prompt (e.g. Cyberpunk Neon City)..."
            placeholderTextColor="#64748b"
            value={prompt}
            onChangeText={setPrompt}
            multiline
          />
          <TouchableOpacity style={[styles.generateButton, (!prompt.trim() || isGenerating) && styles.generateButtonDisabled]} onPress={generateImage} disabled={!prompt.trim() || isGenerating}>
            <Text style={styles.generateButtonText}>Generate</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  // --- LOGIN STYLES ---
  loginContainer: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  bgBlob: {
    position: 'absolute',
    width: 600,
    height: 600,
    borderRadius: 300,
    opacity: 0.15,
  },
  blob1: {
    top: -200,
    left: -200,
    backgroundColor: '#f59e0b',
  },
  blob2: {
    bottom: -200,
    right: -200,
    backgroundColor: '#81542b',
  },
  loginContent: {
    alignItems: 'center',
    padding: 30,
    width: '100%',
    zIndex: 10,
  },
  logoContainer: {
    width: 120,
    height: 120,
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    shadowColor: '#f59e0b',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  logoEmoji: {
    fontSize: 60,
  },
  loginTitle: {
    fontSize: 36,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 10,
    letterSpacing: -1,
  },
  loginSubtitle: {
    fontSize: 16,
    color: '#94a3b8',
    marginBottom: 50,
    textAlign: 'center',
  },
  googleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    paddingVertical: 16,
    paddingHorizontal: 30,
    borderRadius: 100,
    width: '100%',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 5,
    elevation: 5,
  },
  googleIcon: {
    width: 24,
    height: 24,
    marginRight: 12,
  },
  googleButtonText: {
    color: '#1e293b',
    fontSize: 18,
    fontWeight: '700',
  },
  loginTerms: {
    color: '#475569',
    fontSize: 12,
    marginTop: 24,
  },
  
  // --- STUDIO STYLES ---
  safeArea: { flex: 1, backgroundColor: '#0f172a' },
  container: { flex: 1, backgroundColor: '#0f172a' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 20, paddingTop: Platform.OS === 'android' ? 40 : 20 },
  headerTitle: { color: '#ffffff', fontSize: 24, fontWeight: '900' },
  profilePic: { width: 40, height: 40, borderRadius: 20, borderWidth: 2, borderColor: '#334155' },
  scrollContent: { flexGrow: 1, padding: 20 },
  canvasContainer: { width: '100%', aspectRatio: 1, backgroundColor: '#1e293b', borderRadius: 30, overflow: 'hidden', borderWidth: 1, borderColor: '#334155' },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingText: { color: '#94a3b8', marginTop: 16, fontWeight: '600' },
  generatedImage: { width: '100%', height: '100%' },
  placeholderContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  placeholderIcon: { fontSize: 40, marginBottom: 10, opacity: 0.5 },
  placeholderText: { color: '#475569', fontSize: 16, fontWeight: '600' },
  inputDock: { backgroundColor: '#1e293b', padding: 20, borderTopLeftRadius: 30, borderTopRightRadius: 30 },
  input: { backgroundColor: '#0f172a', color: '#ffffff', borderRadius: 20, padding: 20, fontSize: 16, minHeight: 120, textAlignVertical: 'top', marginBottom: 15 },
  generateButton: { backgroundColor: '#f59e0b', borderRadius: 20, paddingVertical: 18, alignItems: 'center' },
  generateButtonDisabled: { opacity: 0.5, backgroundColor: '#334155' },
  generateButtonText: { color: '#000000', fontSize: 18, fontWeight: '900' },
});
