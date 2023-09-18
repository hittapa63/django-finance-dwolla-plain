import React, { useCallback, useState, FunctionComponent } from "react";
import {
  usePlaidLink,
  PlaidLinkOptions,
  PlaidLinkOnSuccess,
} from "react-plaid-link";
import {getAction} from "../../../api";
import {API_ROOT} from "../const";

const PlaidLink = function(props) {
  console.log(props);
    var onSuccess = useCallback(function (public_token, metadata) {
        // send public_token to server
        console.log(public_token);
        console.log(metadata);
        const action = getAction(API_ROOT, ["plaid", "create"]);
        let params = { public_token: public_token, account_id: metadata.account_id != null ? metadata.account_id : metadata.accounts[0].id, link_token: props.customer.customer_id};
        const client = props.client;
        client.action(window.schema, action, params).then((result) => {
          window.location.reload();
        });

    }, []);

  var config = {
    token: props.token,
    onSuccess: onSuccess,
    // onExit
    // onEvent
  };

  const { open, ready, error } = usePlaidLink(config);

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect a bank account
    </button>
  );
};

export default PlaidLink;