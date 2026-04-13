import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Image, ScrollView, ActivityIndicator, SafeAreaView, Dimensions, KeyboardAvoidingView, Platform } from 'react';
import { StatusBar } from 'expo-status-bar';

const { width } = Dimensions.get('window');

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [error, setError] = useState(null);

  const generateImage = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setError(null);
    
    try {
      // Create FormData exactly like the web app
      const formData = new FormData();
      formData.append('chat_id', 'bXYwNi1zZGtkZ3Y');
      formData.append('message', prompt);
      formData.append('does_chat_have_name', 'false');
      formData.append('models', 'ChatGpt');
      formData.append('versions_data', '[{"modelName":"ChatGpt","version":"gpt-3.5-turbo"}]');
      formData.append('requestId', `req_${Date.now()}`);
      
      // Hit the central Azure API directly
      const response = await fetch('https://chatezzy.com/chat/v2/nanobanana-direct', {
        method: 'POST',
        headers: {
          'Accept': '*/*',
          'Origin': 'https://chatezzy.com',
          'Referer': 'https://chatezzy.com/superai/bXYwNi1zZGtkZ3Y',
          'User-Agent': 'NanoBananaAndroid/1.0',
          // Assuming anonymous for the demo, otherwise we pass authToken
        },
        body: formData
      });
      
      const data = await response.json();
      
      // Parse the same way the web UI parses it
      if (data && typeof data === 'object') {
        const lastKey = Object.keys(data).pop();
        const finalChunk = data[lastKey];
        if (finalChunk && finalChunk.images && finalChunk.images.length > 0) {
          setGeneratedImage(finalChunk.images[0]);
        } else {
          setError("Failed to generate image. Please try again.");
        }
      }
    } catch (err) {
      console.error(err);
      setError("Network error. Please check your connection.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="light" />
      <KeyboardAvoidingView 
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.container}
      >
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Nano Banana</Text>
          <View style={styles.proBadge}>
            <Text style={styles.proBadgeText}>PRO</Text>
          </View>
        </View>

        <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
          
          {/* Main Canvas Area */}
          <View style={styles.canvasContainer}>
            {isGenerating ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#f59e0b" />
                <Text style={styles.loadingText}>Rendering your masterpiece...</Text>
              </View>
            ) : generatedImage ? (
              <Image 
                source={{ uri: generatedImage }} 
                style={styles.generatedImage} 
                resizeMode="cover"
              />
            ) : (
              <View style={styles.placeholderContainer}>
                <Text style={styles.placeholderIcon}>✨</Text>
                <Text style={styles.placeholderText}>What do you want to create?</Text>
              </View>
            )}
          </View>
          
          {error && <Text style={styles.errorText}>{error}</Text>}

        </ScrollView>

        {/* Floating Input Dock */}
        <View style={styles.inputDock}>
          <TextInput
            style={styles.input}
            placeholder="Describe your imagination..."
            placeholderTextColor="#9ca3af"
            value={prompt}
            onChangeText={setPrompt}
            multiline
            maxLength={500}
          />
          <TouchableOpacity 
            style={[styles.generateButton, (!prompt.trim() || isGenerating) && styles.generateButtonDisabled]}
            onPress={generateImage}
            disabled={!prompt.trim() || isGenerating}
          >
            <Text style={styles.generateButtonText}>Generate</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  headerTitle: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: '800',
    marginRight: 8,
  },
  proBadge: {
    backgroundColor: '#f59e0b',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  proBadgeText: {
    color: '#000',
    fontSize: 10,
    fontWeight: '900',
  },
  scrollContent: {
    flexGrow: 1,
    padding: 16,
  },
  canvasContainer: {
    width: '100%',
    aspectRatio: 1,
    backgroundColor: '#1e293b',
    borderRadius: 24,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#334155',
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 16,
    fontWeight: '600',
  },
  generatedImage: {
    width: '100%',
    height: '100%',
  },
  placeholderContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  placeholderIcon: {
    fontSize: 48,
    marginBottom: 16,
  },
  placeholderText: {
    color: '#64748b',
    fontSize: 16,
    textAlign: 'center',
    fontWeight: '500',
  },
  errorText: {
    color: '#ef4444',
    textAlign: 'center',
    marginTop: 16,
    fontWeight: '600',
  },
  inputDock: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#334155',
    paddingBottom: Platform.OS === 'ios' ? 32 : 16,
  },
  input: {
    backgroundColor: '#0f172a',
    color: '#ffffff',
    borderRadius: 16,
    padding: 16,
    fontSize: 16,
    minHeight: 100,
    textAlignVertical: 'top',
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 16,
  },
  generateButton: {
    backgroundColor: '#f59e0b',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
  },
  generateButtonDisabled: {
    opacity: 0.5,
  },
  generateButtonText: {
    color: '#000000',
    fontSize: 18,
    fontWeight: '800',
  },
});
