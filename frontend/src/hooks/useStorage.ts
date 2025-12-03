/**
 * ALSHAM QUANTUM - Storage Hook
 * Simplified interface for Supabase Storage operations
 */

import { useState } from 'react';
import { supabase } from '@/lib/supabase';

export type StorageBucket = 'avatars' | 'documents' | 'exports';

interface UploadOptions {
  onProgress?: (progress: number) => void;
  cacheControl?: string;
  upsert?: boolean;
}

interface UploadResult {
  path: string;
  fullPath: string;
  publicUrl?: string;
}

export function useStorage() {
  const [uploading, setUploading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Upload a file to a storage bucket
   */
  const uploadFile = async (
    bucket: StorageBucket,
    file: File,
    options: UploadOptions = {}
  ): Promise<UploadResult | null> => {
    try {
      setUploading(true);
      setError(null);

      // Generate unique filename
      const fileExt = file.name.split('.').pop();
      const fileName = `${Date.now()}_${Math.random().toString(36).substring(7)}.${fileExt}`;
      const filePath = fileName;

      // Upload to Supabase Storage
      const { data, error: uploadError } = await supabase.storage
        .from(bucket)
        .upload(filePath, file, {
          cacheControl: options.cacheControl || '3600',
          upsert: options.upsert || false,
        });

      if (uploadError) {
        throw uploadError;
      }

      // Get public URL if bucket is public (avatars)
      let publicUrl: string | undefined;
      if (bucket === 'avatars') {
        const { data: urlData } = supabase.storage
          .from(bucket)
          .getPublicUrl(filePath);
        publicUrl = urlData.publicUrl;
      }

      const result: UploadResult = {
        path: data.path,
        fullPath: `${bucket}/${data.path}`,
        publicUrl,
      };

      setUploading(false);
      return result;

    } catch (err) {
      console.error('❌ Upload error:', err);
      setError(err instanceof Error ? err.message : 'Upload failed');
      setUploading(false);
      return null;
    }
  };

  /**
   * Download a file from a storage bucket
   */
  const downloadFile = async (
    bucket: StorageBucket,
    path: string
  ): Promise<Blob | null> => {
    try {
      setDownloading(true);
      setError(null);

      const { data, error: downloadError } = await supabase.storage
        .from(bucket)
        .download(path);

      if (downloadError) {
        throw downloadError;
      }

      setDownloading(false);
      return data;

    } catch (err) {
      console.error('❌ Download error:', err);
      setError(err instanceof Error ? err.message : 'Download failed');
      setDownloading(false);
      return null;
    }
  };

  /**
   * Delete a file from a storage bucket
   */
  const deleteFile = async (
    bucket: StorageBucket,
    path: string
  ): Promise<boolean> => {
    try {
      setError(null);

      const { error: deleteError } = await supabase.storage
        .from(bucket)
        .remove([path]);

      if (deleteError) {
        throw deleteError;
      }

      return true;

    } catch (err) {
      console.error('❌ Delete error:', err);
      setError(err instanceof Error ? err.message : 'Delete failed');
      return false;
    }
  };

  /**
   * Get public URL for a file (works only for public buckets)
   */
  const getPublicUrl = (bucket: StorageBucket, path: string): string | null => {
    try {
      if (bucket !== 'avatars') {
        console.warn('⚠️ getPublicUrl only works for public buckets (avatars)');
        return null;
      }

      const { data } = supabase.storage
        .from(bucket)
        .getPublicUrl(path);

      return data.publicUrl;

    } catch (err) {
      console.error('❌ Get public URL error:', err);
      setError(err instanceof Error ? err.message : 'Failed to get public URL');
      return null;
    }
  };

  /**
   * Get signed URL for a file (works for private buckets)
   */
  const getSignedUrl = async (
    bucket: StorageBucket,
    path: string,
    expiresIn: number = 3600 // 1 hour default
  ): Promise<string | null> => {
    try {
      const { data, error: signError } = await supabase.storage
        .from(bucket)
        .createSignedUrl(path, expiresIn);

      if (signError) {
        throw signError;
      }

      return data.signedUrl;

    } catch (err) {
      console.error('❌ Get signed URL error:', err);
      setError(err instanceof Error ? err.message : 'Failed to get signed URL');
      return null;
    }
  };

  /**
   * List files in a bucket folder
   */
  const listFiles = async (
    bucket: StorageBucket,
    path: string = ''
  ): Promise<any[] | null> => {
    try {
      const { data, error: listError } = await supabase.storage
        .from(bucket)
        .list(path, {
          limit: 100,
          offset: 0,
          sortBy: { column: 'created_at', order: 'desc' },
        });

      if (listError) {
        throw listError;
      }

      return data;

    } catch (err) {
      console.error('❌ List files error:', err);
      setError(err instanceof Error ? err.message : 'Failed to list files');
      return null;
    }
  };

  return {
    uploading,
    downloading,
    error,
    uploadFile,
    downloadFile,
    deleteFile,
    getPublicUrl,
    getSignedUrl,
    listFiles,
  };
}
