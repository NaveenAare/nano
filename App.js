
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Image, ScrollView, ActivityIndicator, SafeAreaView, KeyboardAvoidingView, Platform, Animated, Easing, useColorScheme } from 'react-native';
import { StatusBar } from 'expo-status-bar';

// Simulated Auth Session for now until we configure Google Cloud Console
export default function App() {
  const colorScheme = useColorScheme(); // detects light/dark mode based on device/time
  const isDarkMode = colorScheme === 'dark';

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

  const getThemeStyles = () => {
    return isDarkMode ? darkStyles : lightStyles;
  };
  const currentStyles = getThemeStyles();

  // --- LOGIN SCREEN ---
  if (!isAuthenticated) {
    return (
      <View style={[styles.loginContainer, currentStyles.bgMain]}>
        <StatusBar style={isDarkMode ? "light" : "dark"} />
        
        {/* Animated 3D Background Elements */}
        <Animated.View style={[styles.bgBlob, styles.blob1, { transform: [{ rotate: spin }] }]} />
        <Animated.View style={[styles.bgBlob, styles.blob2, { transform: [{ rotate: spin }] }]} />
        
        <View style={styles.loginContent}>
          <Animated.View style={[styles.logoContainer, currentStyles.logoBox, { transform: [{ translateY }] }]}>
            <Text style={styles.logoEmoji}>🍌</Text>
          </Animated.View>
          
          <Animated.Text style={[styles.loginTitle, currentStyles.textPrimary, { opacity: fadeValue }]}>Nano Banana</Animated.Text>
          <Animated.Text style={[styles.loginSubtitle, currentStyles.textSecondary, { opacity: fadeValue }]}>Masterpiece Generation, Instantly.</Animated.Text>
          
          <TouchableOpacity style={[styles.googleButton, currentStyles.googleBtnBg]} onPress={handleLogin} activeOpacity={0.8}>
            <Image 
              source={{ uri: 'https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg' }} 
              style={styles.googleIcon} 
            />
            <Text style={[styles.googleButtonText, currentStyles.googleBtnText]}>Continue with Google</Text>
          </TouchableOpacity>
          
          <Text style={[styles.loginTerms, currentStyles.textSecondary]}>By continuing, you agree to our Terms of Service</Text>
        </View>
      </View>
    );
  }

  // --- MAIN STUDIO SCREEN ---
  return (
    <SafeAreaView style={[styles.safeArea, currentStyles.bgMain]}>
      <StatusBar style={isDarkMode ? "light" : "dark"} />
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={[styles.container, currentStyles.bgMain]}>
        <View style={[styles.header, currentStyles.headerBorder]}>
          <Text style={[styles.headerTitle, currentStyles.textPrimary]}>Studio</Text>
          <TouchableOpacity onPress={() => setIsAuthenticated(false)}>
            <Image source={{ uri: 'https://ui-avatars.com/api/?name=User&background=f59e0b&color=000' }} style={styles.profilePic} />
          </TouchableOpacity>
        </View>

        <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
          <View style={[styles.canvasContainer, currentStyles.canvasBg, currentStyles.canvasBorder]}>
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
                <Text style={[styles.placeholderText, currentStyles.textSecondary]}>Describe your masterpiece...</Text>
              </View>
            )}
          </View>
        </ScrollView>

        <View style={[styles.inputDock, currentStyles.dockBg]}>
          <TextInput
            style={[styles.input, currentStyles.inputBg, currentStyles.textPrimary, currentStyles.canvasBorder]}
            placeholder="Type a prompt (e.g. Cyberpunk Neon City)..."
            placeholderTextColor={isDarkMode ? "#64748b" : "#94a3b8"}
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
  // --- BASE STYLES ---
  loginContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', overflow: 'hidden' },
  bgBlob: { position: 'absolute', width: 600, height: 600, borderRadius: 300, opacity: 0.15 },
  blob1: { top: -200, left: -200, backgroundColor: '#f59e0b' },
  blob2: { bottom: -200, right: -200, backgroundColor: '#81542b' },
  loginContent: { alignItems: 'center', padding: 30, width: '100%', zIndex: 10 },
  logoContainer: { width: 120, height: 120, borderRadius: 40, justifyContent: 'center', alignItems: 'center', marginBottom: 30, borderWidth: 1, shadowColor: '#f59e0b', shadowOffset: { width: 0, height: 10 }, shadowOpacity: 0.3, shadowRadius: 20, elevation: 10 },
  logoEmoji: { fontSize: 60 },
  loginTitle: { fontSize: 36, fontWeight: '900', marginBottom: 10, letterSpacing: -1 },
  loginSubtitle: { fontSize: 16, marginBottom: 50, textAlign: 'center' },
  googleButton: { flexDirection: 'row', alignItems: 'center', paddingVertical: 16, paddingHorizontal: 30, borderRadius: 100, width: '100%', justifyContent: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 5, elevation: 5 },
  googleIcon: { width: 24, height: 24, marginRight: 12 }, // Google logo SVG will render here
  googleButtonText: { fontSize: 18, fontWeight: '700' },
  loginTerms: { fontSize: 12, marginTop: 24 },
  
  safeArea: { flex: 1 },
  container: { flex: 1 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 20, paddingTop: Platform.OS === 'android' ? 40 : 20, borderBottomWidth: 1 },
  headerTitle: { fontSize: 24, fontWeight: '900' },
  profilePic: { width: 40, height: 40, borderRadius: 20, borderWidth: 2, borderColor: '#f59e0b' },
  scrollContent: { flexGrow: 1, padding: 20 },
  canvasContainer: { width: '100%', aspectRatio: 1, borderRadius: 30, overflow: 'hidden', borderWidth: 1, elevation: 10, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 8 },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingText: { color: '#94a3b8', marginTop: 16, fontWeight: '600' },
  generatedImage: { width: '100%', height: '100%' },
  placeholderContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  placeholderIcon: { fontSize: 40, marginBottom: 10, opacity: 0.5 },
  placeholderText: { fontSize: 16, fontWeight: '600' },
  inputDock: { padding: 20, borderTopLeftRadius: 30, borderTopRightRadius: 30 },
  input: { borderRadius: 20, padding: 20, fontSize: 16, minHeight: 120, textAlignVertical: 'top', marginBottom: 15, borderWidth: 1 },
  generateButton: { backgroundColor: '#f59e0b', borderRadius: 20, paddingVertical: 18, alignItems: 'center' },
  generateButtonDisabled: { opacity: 0.5 },
  generateButtonText: { color: '#000000', fontSize: 18, fontWeight: '900' },
});

const darkStyles = StyleSheet.create({
  bgMain: { backgroundColor: '#0f172a' },
  textPrimary: { color: '#ffffff' },
  textSecondary: { color: '#94a3b8' },
  logoBox: { backgroundColor: 'rgba(255,255,255,0.05)', borderColor: 'rgba(255,255,255,0.1)' },
  googleBtnBg: { backgroundColor: '#ffffff' },
  googleBtnText: { color: '#1e293b' },
  headerBorder: { borderBottomColor: '#1e293b' },
  canvasBg: { backgroundColor: '#1e293b' },
  canvasBorder: { borderColor: '#334155' },
  dockBg: { backgroundColor: '#1e293b' },
  inputBg: { backgroundColor: '#0f172a' },
});

const lightStyles = StyleSheet.create({
  bgMain: { backgroundColor: '#f8fafc' },
  textPrimary: { color: '#0f172a' },
  textSecondary: { color: '#64748b' },
  logoBox: { backgroundColor: '#ffffff', borderColor: '#e2e8f0', shadowColor: '#f59e0b' },
  googleBtnBg: { backgroundColor: '#1e293b' },
  googleBtnText: { color: '#ffffff' },
  headerBorder: { borderBottomColor: '#e2e8f0' },
  canvasBg: { backgroundColor: '#ffffff' },
  canvasBorder: { borderColor: '#e2e8f0' },
  dockBg: { backgroundColor: '#ffffff' },
  inputBg: { backgroundColor: '#f1f5f9' },
});
