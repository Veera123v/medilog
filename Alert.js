import React from 'react';
import { Snackbar, Alert as MuiAlert } from '@mui/material';

const Alert = ({ error, clearErrors }) => {
  return (
    <Snackbar
      open={!!error}
      autoHideDuration={6000}
      onClose={clearErrors}
      anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
    >
      <MuiAlert onClose={clearErrors} severity="error" elevation={6} variant="filled">
        {error}
      </MuiAlert>
    </Snackbar>
  );
};

export default Alert;
